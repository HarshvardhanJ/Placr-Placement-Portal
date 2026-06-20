<template>
  <DashboardLayout>
    <PageHeader
      title="Drives"
      subtitle="Manage placement drives, approvals, and status."
    >
      <template #actions>
        <button
          type="button"
          class="btn btn-primary d-inline-flex align-items-center gap-2"
        >
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
          >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
            <path d="M7 11l5 5l5 -5" />
            <path d="M12 4l0 12" />
          </svg>
          <span>Export</span>
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
              <option value="approved">Approved</option>
              <option value="pending">Pending</option>
              <option value="closed">Closed</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          <div class="col-lg-2">
            <button
              class="btn btn-outline-secondary w-100"
              type="button"
              @click="clearFilters"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <DataTable title="Drives" :headers="headers" :rows="filteredDrives">
      <template #status="{ row }">
        <span class="badge rounded-pill" :class="statusBadgeClass(row.status)">
          {{ row.status }}
        </span>
      </template>

      <template #actions="{ row }">
        <div class="d-flex flex-wrap gap-2">
          <button
            class="btn btn-sm btn-outline-primary"
            @click="viewDrive(row)"
          >
            View
          </button>

          <button
            v-if="row.status === 'Pending'"
            class="btn btn-sm btn-outline-success"
            @click="approveDrive(row)"
          >
            Approve
          </button>

          <button
            v-if="row.status === 'Approved'"
            class="btn btn-sm btn-outline-warning"
            @click="confirmClose(row)"
          >
            Close
          </button>

          <button
            v-if="row.status !== 'Rejected'"
            class="btn btn-sm btn-outline-danger"
            @click="confirmReject(row)"
          >
            Reject
          </button>
        </div>
      </template>
    </DataTable>

    <div v-if="showDriveModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header">
            <div>
              <h5 class="modal-title mb-1">Drive Details</h5>
              <small class="text-secondary">Placement drive overview</small>
            </div>
            <button
              type="button"
              class="btn-close"
              @click="showDriveModal = false"
            ></button>
          </div>

          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="text-secondary">Company</label>
                <div class="fw-medium">{{ selectedDrive?.company }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Industry</label>
                <div class="fw-medium">{{ selectedDrive?.industry }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Role</label>
                <div class="fw-medium">{{ selectedDrive?.role }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Deadline</label>
                <div class="fw-medium">{{ selectedDrive?.deadline }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Applicants</label>
                <div class="fw-medium">{{ selectedDrive?.applicants }}</div>
              </div>

              <div class="col-md-6">
                <label class="text-secondary">Status</label>
                <div class="fw-medium">{{ selectedDrive?.status }}</div>
              </div>

              <div class="col-12">
                <label class="text-secondary">Description</label>
                <div class="fw-medium">{{ selectedDrive?.description }}</div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showDriveModal = false">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showDriveModal" class="modal-backdrop fade show"></div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from "vue";

import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";
import StatCard from "@/components/shared/StatCard.vue";

const searchQuery = ref("");
const statusFilter = ref("");

const selectedDrive = ref(null);
const showDriveModal = ref(false);

const drives = ref([
  {
    id: 1,
    company: "Google",
    industry: "Technology",
    role: "SDE Intern",
    deadline: "2026-07-10",
    applicants: 125,
    status: "Approved",
    description: "Campus hiring drive for summer internship roles.",
  },
  {
    id: 2,
    company: "Amazon",
    industry: "Technology",
    role: "Backend Intern",
    deadline: "2026-07-15",
    applicants: 87,
    status: "Pending",
    description: "Hiring for backend-focused internship positions.",
  },
  {
    id: 3,
    company: "NVIDIA",
    industry: "Semiconductors",
    role: "ML Intern",
    deadline: "2026-07-05",
    applicants: 42,
    status: "Closed",
    description: "Closed drive for machine learning internship roles.",
  },
  {
    id: 4,
    company: "Adobe",
    industry: "Software",
    role: "Product Intern",
    deadline: "2026-07-20",
    applicants: 65,
    status: "Rejected",
    description: "Rejected due to incomplete eligibility details.",
  },
]);

const headers = [
  { key: "company", label: "Company" },
  { key: "industry", label: "Industry" },
  { key: "role", label: "Role" },
  { key: "deadline", label: "Deadline" },
  { key: "applicants", label: "Applicants" },
  { key: "status", label: "Status" },
  { key: "actions", label: "Actions" },
];

const stats = computed(() => [
  { title: "Total Drives", value: drives.value.length },
  {
    title: "Approved",
    value: drives.value.filter((d) => d.status === "Approved").length,
  },
  {
    title: "Pending",
    value: drives.value.filter((d) => d.status === "Pending").length,
  },
  {
    title: "Closed",
    value: drives.value.filter((d) => d.status === "Closed").length,
  },
]);

const filteredDrives = computed(() => {
  return drives.value.filter((drive) => {
    const query = searchQuery.value.toLowerCase();

    const matchesSearch =
      drive.company.toLowerCase().includes(query) ||
      drive.role.toLowerCase().includes(query) ||
      drive.industry.toLowerCase().includes(query);

    const matchesStatus =
      !statusFilter.value || drive.status.toLowerCase() === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const clearFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
};

const statusBadgeClass = (status) => {
  switch (status) {
    case "Approved":
      return "text-bg-success";
    case "Pending":
      return "text-bg-warning";
    case "Closed":
      return "text-bg-secondary";
    case "Rejected":
      return "text-bg-danger";
    default:
      return "text-bg-light";
  }
};

const viewDrive = (drive) => {
  selectedDrive.value = drive;
  showDriveModal.value = true;
};

const approveDrive = (drive) => {
  drive.status = "Approved";
};

const closeDrive = (drive) => {
  drive.status = "Closed";
};

const confirmClose = (drive) => {
  if (window.confirm(`Close ${drive.company} - ${drive.role}?`)) {
    closeDrive(drive);
  }
};

const rejectDrive = (drive) => {
  drives.value = drives.value.filter((d) => d.id !== drive.id);
};

const confirmReject = (drive) => {
  if (window.confirm(`Reject ${drive.company} - ${drive.role}?`)) {
    rejectDrive(drive);
  }
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
