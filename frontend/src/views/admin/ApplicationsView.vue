<template>
  <DashboardLayout>
    <PageHeader
      title="Applications"
      subtitle="Monitor and search all job applications across the platform."
    >
      <template #actions>
        <button type="button" class="btn btn-primary">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="icon icon-tabler icons-tabler-outline icon-tabler-download"
          >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
            <path d="M7 11l5 5l5 -5" />
            <path d="M12 4l0 12" />
          </svg>
          Export
        </button>
      </template>
    </PageHeader>

    <div class="row g-3 mb-4">
      <div
        v-for="stat in stats"
        :key="stat.title"
        class="col-12 col-sm-6 col-xl-3"
      >
        <StatCard :title="stat.title" :value="stat.value" />
      </div>
    </div>

    <div class="card shadow-sm border-0 mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-center">
          <div class="col-lg-7">
            <div class="search-wrap">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="search-icon"
              >
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>

              <input
                v-model="searchQuery"
                type="text"
                class="form-control border-0 shadow-none"
                placeholder="Search by company, role, or industry..."
              />
            </div>
          </div>

          <div class="col-lg-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">All Statuses</option>
              <option value="applied">Applied</option>
              <option value="shortlisted">Shortlisted</option>
              <option value="selected">Selected</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          <div class="col-lg-2">
            <button
              class="btn btn-outline-secondary w-100"
              @click="clearFilters"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <DataTable
      title="Applications"
      :headers="headers"
      :rows="filteredApplications"
    >
      <template #status="{ row }">
        <span class="badge rounded-pill" :class="statusBadgeClass(row.status)">
          {{ formatStatus(row.status) }}
        </span>
      </template>

      <template #actions="{ row }">
        <div class="d-flex gap-2">
          <button
            class="btn btn-sm btn-outline-primary"
            @click="viewApplication(row)"
          >
            View
          </button>
        </div>
      </template>
    </DataTable>

    <div v-if="showApplicationModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <div>
              <h5 class="modal-title mt-2 mb-1">Application Details</h5>
            </div>
            <button
              type="button"
              class="btn-close"
              @click="showApplicationModal = false"
            ></button>
          </div>

          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="text-secondary">Student Name</label>
                <div class="fw-medium">
                  {{ selectedApplication?.student_name }}
                </div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Roll No</label>
                <div class="fw-medium">{{ selectedApplication?.roll_no }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Company</label>
                <div class="fw-medium">{{ selectedApplication?.company }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Job Title</label>
                <div class="fw-medium">
                  {{ selectedApplication?.job_title }}
                </div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Status</label>
                <div class="fw-medium">
                  {{ formatStatus(selectedApplication?.status) }}
                </div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Applied On</label>
                <div class="fw-medium">
                  {{ selectedApplication?.application_date }}
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button
              class="btn btn-secondary"
              @click="showApplicationModal = false"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showApplicationModal" class="modal-backdrop fade show"></div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

import api from "@/services/api";
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";
import StatCard from "@/components/shared/StatCard.vue";

const searchQuery = ref("");
const statusFilter = ref("");

const selectedApplication = ref(null);
const showApplicationModal = ref(false);

const applications = ref([
  {
    application_id: 1,
    student_name: "Rahul Sharma",
    roll_no: "24CS101",
    company: "Google",
    job_title: "SDE Intern",
    status: "applied",
    application_date: "2026-06-15",
  },
  {
    application_id: 2,
    student_name: "Priya Nair",
    roll_no: "24EC205",
    company: "Amazon",
    job_title: "Backend Intern",
    status: "shortlisted",
    application_date: "2026-06-14",
  },
  {
    application_id: 3,
    student_name: "Aman Verma",
    roll_no: "24ME112",
    company: "NVIDIA",
    job_title: "ML Intern",
    status: "selected",
    application_date: "2026-06-12",
  },
  {
    application_id: 4,
    student_name: "Sneha Iyer",
    roll_no: "24CS143",
    company: "Adobe",
    job_title: "Product Intern",
    status: "rejected",
    application_date: "2026-06-11",
  },
  {
    application_id: 5,
    student_name: "Arjun Menon",
    roll_no: "24EE087",
    company: "Microsoft",
    job_title: "Software Intern",
    status: "applied",
    application_date: "2026-06-18",
  },
  {
    application_id: 6,
    student_name: "Meera Nair",
    roll_no: "24CS127",
    company: "Goldman Sachs",
    job_title: "Summer Analyst",
    status: "shortlisted",
    application_date: "2026-06-17",
  },
]);

const headers = [
  { key: "student_name", label: "Student" },
  { key: "roll_no", label: "Roll No" },
  { key: "company", label: "Company" },
  { key: "job_title", label: "Role" },
  { key: "status", label: "Status" },
  { key: "application_date", label: "Applied On" },
  { key: "actions", label: "Actions" },
];

const clearFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
};

const stats = computed(() => [
  {
    title: "Applications",
    value: applications.value.length,
  },
  {
    title: "Applied",
    value: applications.value.filter((a) => a.status === "applied").length,
  },
  {
    title: "Shortlisted",
    value: applications.value.filter((a) => a.status === "shortlisted").length,
  },
  {
    title: "Selected",
    value: applications.value.filter((a) => a.status === "selected").length,
  },
]);
// const loadApplications = async () => {
//   try {
//     const response = await api.get("/admin/applications");
//     applications.value = response.data;
//   } catch (error) {
//     console.error("Failed to load applications:", error);
//   }
// };

onMounted(() => {
  // loadApplications();
});

const statusBadgeClass = (status) => {
  switch (status) {
    case "applied":
      return "text-bg-secondary";

    case "shortlisted":
      return "text-bg-warning";

    case "selected":
      return "text-bg-success";

    case "rejected":
      return "text-bg-danger";

    default:
      return "text-bg-light";
  }
};

const filteredApplications = computed(() => {
  return applications.value.filter((application) => {
    const query = searchQuery.value.toLowerCase();

    const matchesSearch =
      application.student_name.toLowerCase().includes(query) ||
      application.roll_no.toLowerCase().includes(query) ||
      application.company.toLowerCase().includes(query) ||
      application.job_title.toLowerCase().includes(query);

    const matchesStatus =
      !statusFilter.value ||
      application.status.toLowerCase() === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const totalApplications = computed(() => applications.value.length);
const appliedCount = computed(
  () => applications.value.filter((a) => a.status === "applied").length,
);
const shortlistedCount = computed(
  () => applications.value.filter((a) => a.status === "shortlisted").length,
);
const selectedCount = computed(
  () => applications.value.filter((a) => a.status === "selected").length,
);

const viewApplication = (application) => {
  selectedApplication.value = application;
  showApplicationModal.value = true;
};

const formatStatus = (status) => {
  if (!status) return "";
  return status.charAt(0).toUpperCase() + status.slice(1);
};
</script>

<style scoped>
.search-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f8fafc;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  padding: 0.6rem 0.9rem;
}

.search-icon {
  color: #6b7280;
  flex-shrink: 0;
}
</style>
