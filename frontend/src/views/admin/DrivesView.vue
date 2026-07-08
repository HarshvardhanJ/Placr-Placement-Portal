<template>
  <DashboardLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Drives"
      subtitle="Manage placement drives, approvals, and status."
    />

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
                placeholder="Search by company, role, or location..."
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
        <div class="d-flex flex-wrap gap-2 justify-content-end">
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
            v-if="row.status === 'Pending'"
            class="btn btn-sm btn-outline-danger"
            @click="confirmReject(row)"
          >
            Reject
          </button>

          <button
            v-if="row.status === 'Approved'"
            class="btn btn-sm btn-outline-warning"
            @click="confirmClose(row)"
          >
            Close
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
                <label class="text-secondary">Location</label>
                <div class="fw-medium">{{ selectedDrive?.location }}</div>
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

              <div class="col-md-6">
                <label class="text-secondary">Eligible Branches</label>
                <div class="fw-medium">
                  {{ selectedDrive?.eligible_branch || "All branches" }}
                </div>
              </div>

              <div class="col-12">
                <label class="text-secondary">Description</label>
                <div class="fw-medium">
                  {{ selectedDrive?.description || "No description provided." }}
                </div>
              </div>

              <div class="col-12">
                <label class="text-secondary">Requirements</label>
                <div class="d-flex flex-wrap gap-2">
                  <span class="badge text-bg-light border"
                    >CGPA ≥ {{ selectedDrive?.min_cgpa ?? "—" }}</span
                  >
                  <span class="badge text-bg-light border"
                    >Openings: {{ selectedDrive?.no_openings ?? "—" }}</span
                  >
                  <span class="badge text-bg-light border"
                    >Salary: {{ formatCurrency(selectedDrive?.salary) }}</span
                  >
                </div>
              </div>

              <div class="col-12">
                <label class="text-secondary"
                  >Skills / Experience / Benefits</label
                >
                <div class="small text-secondary mt-1">
                  <div>
                    <strong>Skills:</strong>
                    {{ selectedDrive?.required_skills || "—" }}
                  </div>
                  <div>
                    <strong>Experience:</strong>
                    {{ selectedDrive?.experience_required || "—" }}
                  </div>
                  <div>
                    <strong>Benefits:</strong>
                    {{ selectedDrive?.benefits || "—" }}
                  </div>
                </div>
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
import { ref, computed, onMounted } from "vue";
import api from "@/services/api";
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";
import StatCard from "@/components/shared/StatCard.vue";

const searchQuery = ref("");
const statusFilter = ref("");

const selectedDrive = ref(null);
const showDriveModal = ref(false);
const loading = ref(false);
const drives = ref([]);

const loadDrives = async () => {
  try {
    loading.value = true;

    const response = await api.get("/admin/drives");

    drives.value = response.data.map((drive) => ({
      ...drive,

      company: drive.company_name,
      role: drive.job_title,
      deadline: new Date(drive.application_deadline).toLocaleDateString(),

      applicants: drive.applicants ?? 0,

      status:
        drive.approval_status.charAt(0).toUpperCase() +
        drive.approval_status.slice(1),

      description: drive.job_description,
      location: drive.job_location,
      eligible_branch: drive.eligible_branch,
      min_cgpa: drive.min_cgpa,
      no_openings: drive.no_openings,
      salary: drive.salary,
      required_skills: drive.required_skills,
      experience_required: drive.experience_required,
      benefits: drive.benefits,
    }));
  } catch (error) {
    console.error("Failed to load drives:", error);
  } finally {
    loading.value = false;
  }
};

const headers = [
  { key: "company", label: "Company" },
  { key: "job_location", label: "Location" },
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
      (drive.company || "").toLowerCase().includes(query) ||
      (drive.role || "").toLowerCase().includes(query) ||
      (drive.required_skills || "").toLowerCase().includes(query) ||
      (drive.location || drive.job_location || "")
        .toLowerCase()
        .includes(query);

    const matchesStatus =
      !statusFilter.value || drive.status.toLowerCase() === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const clearFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
};

const formatCurrency = (value) => {
  if (value === null || value === undefined || value === "") return "—";
  const num = Number(value);
  if (Number.isNaN(num)) return String(value);
  return `₹${num.toLocaleString("en-IN")}`;
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

const approveDrive = async (drive) => {
  try {
    await api.put(`/admin/drives/${drive.drive_id}/approve`);

    drive.status = "Approved";
  } catch (error) {
    console.error(error);
  }
};

const confirmClose = (drive) => {
  if (window.confirm(`Close ${drive.company} - ${drive.role}?`)) {
    closeDrive(drive);
  }
};

const rejectDrive = async (drive) => {
  try {
    await api.put(`/admin/drives/${drive.drive_id}/reject`);

    drive.status = "Rejected";
  } catch (error) {
    console.error(error);
  }
};

const confirmReject = (drive) => {
  if (window.confirm(`Reject ${drive.company} - ${drive.role}?`)) {
    rejectDrive(drive);
  }
};

const formatStatus = (status) => {
  switch (status) {
    case "approved":
      return "Approved";

    case "pending":
      return "Pending";

    case "rejected":
      return "Rejected";

    case "closed":
      return "Closed";

    default:
      return status;
  }
};

const closeDrive = async (drive) => {
  try {
    await api.put(`/admin/drives/${drive.drive_id}/close`);

    drive.status = "Closed";
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  loadDrives();
});
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
