<template>
  <CompanyLayout v-model:search-query="searchQuery">
    <PageHeader
      :title="drive?.job_title || 'Drive Details'"
      subtitle="Review applicants, shortlist candidates, and manage the drive lifecycle."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink to="/company/drives" class="btn btn-outline-secondary">
            <i class="ti ti-arrow-left me-2"></i>Back
          </RouterLink>
          <button
            v-if="canEdit"
            type="button"
            class="btn btn-outline-primary"
            @click="openEditModal"
          >
            <i class="ti ti-pencil me-2"></i>Edit Drive
          </button>
          <button
            v-if="drive && drive.approval_status !== 'closed'"
            type="button"
            class="btn btn-outline-warning"
            @click="confirmClose"
          >
            <i class="ti ti-lock me-2"></i>Close Drive
          </button>
        </div>
      </template>
    </PageHeader>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="loading" class="card shadow-sm p-5 text-center">
      Loading drive details...
    </div>

    <template v-else>
      <div class="row g-3 mb-4">
        <div
          v-for="stat in stats"
          :key="stat.key"
          class="col-12 col-sm-6 col-xl-3"
        >
          <StatCard :title="stat.label" :value="stat.value" :icon="stat.icon" />
        </div>
      </div>

      <div class="row g-4 mb-4">
        <div class="col-12 col-lg-8">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
              <div
                class="d-flex flex-wrap gap-2 align-items-start justify-content-between mb-3"
              >
                <div>
                  <h5 class="mb-1 fw-semibold">{{ drive?.job_title }}</h5>
                  <div class="text-muted">
                    {{ drive?.job_location || "Location not specified" }}
                  </div>
                </div>
                <span
                  class="badge rounded-pill"
                  :class="statusBadgeClass(drive?.approval_status)"
                >
                  {{ formatStatus(drive?.approval_status) }}
                </span>
              </div>

              <p class="text-muted mb-4">
                {{ drive?.job_description || "No job description provided." }}
              </p>

              <div class="row g-3">
                <div class="col-md-6">
                  <label class="text-secondary small">Deadline</label>
                  <div class="fw-semibold">
                    {{ formatDateTime(drive?.application_deadline) }}
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="text-secondary small">Openings</label>
                  <div class="fw-semibold">{{ drive?.no_openings ?? "—" }}</div>
                </div>
                <div class="col-md-6">
                  <label class="text-secondary small">Minimum CGPA</label>
                  <div class="fw-semibold">{{ drive?.min_cgpa ?? "—" }}</div>
                </div>
                <div class="col-md-6">
                  <label class="text-secondary small">Eligible Year</label>
                  <div class="fw-semibold">{{ drive?.year ?? "Any" }}</div>
                </div>
                <div class="col-md-6">
                  <label class="text-secondary small">Salary</label>
                  <div class="fw-semibold">
                    {{ formatCurrency(drive?.salary) }}
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="text-secondary small">Eligible Branches</label>
                  <div class="fw-semibold">
                    {{ drive?.eligible_branch || "All branches" }}
                  </div>
                </div>
                <div class="col-12" v-if="drive?.required_skills">
                  <label class="text-secondary small">Required Skills</label>
                  <div>{{ drive?.required_skills }}</div>
                </div>
                <div class="col-12" v-if="drive?.experience_required">
                  <label class="text-secondary small"
                    >Experience Required</label
                  >
                  <div>{{ drive?.experience_required }}</div>
                </div>
                <div class="col-12" v-if="drive?.benefits">
                  <label class="text-secondary small">Benefits</label>
                  <div>{{ drive?.benefits }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12 col-lg-4">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body d-flex flex-column gap-3">
              <div>
                <h6 class="fw-semibold mb-1">Applicants Pipeline</h6>
                <p class="text-muted small mb-0">
                  Quick snapshot of the current drive progress.
                </p>
              </div>

              <div class="pipeline-item">
                <span>Applied</span>
                <strong>{{ pipeline.applied }}</strong>
              </div>
              <div class="pipeline-item">
                <span>Shortlisted</span>
                <strong>{{ pipeline.shortlisted }}</strong>
              </div>
              <div class="pipeline-item">
                <span>Selected</span>
                <strong>{{ pipeline.selected }}</strong>
              </div>
              <div class="pipeline-item">
                <span>Rejected</span>
                <strong>{{ pipeline.rejected }}</strong>
              </div>

              <RouterLink
                :to="`/company/applications?drive=${driveId}`"
                class="btn btn-primary mt-auto"
              >
                View in Applications
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <div class="card shadow-sm border-0 mb-4">
        <div class="card-body">
          <div class="row g-3 align-items-end">
            <div class="col-lg-4">
              <label class="form-label mb-1">Status Filter</label>
              <select v-model="statusFilter" class="form-select">
                <option value="">All</option>
                <option value="applied">Applied</option>
                <option value="shortlisted">Shortlisted</option>
                <option value="selected">Selected</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
            <div class="col-lg-4">
              <label class="form-label mb-1">Search</label>
              <input
                v-model="searchQuery"
                type="text"
                class="form-control"
                placeholder="Student name, roll no, or department"
              />
            </div>
            <div class="col-lg-4 d-flex gap-2">
              <button
                type="button"
                class="btn btn-outline-secondary flex-fill"
                @click="clearFilters"
              >
                Clear
              </button>
              <button
                type="button"
                class="btn btn-outline-primary flex-fill"
                @click="loadApplications()"
              >
                <i class="ti ti-refresh me-1"></i>Refresh
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="loadingApplications" class="card shadow-sm p-5 text-center">
        Loading applications...
      </div>

      <DataTable
        v-else
        title="Applicants"
        :headers="headers"
        :rows="filteredApplications"
      >
        <template #student_name="{ row }">
          <div class="fw-semibold">{{ row.student_name }}</div>
          <small class="text-muted">{{ row.roll_no }}</small>
        </template>

        <template #department="{ row }">
          {{ row.department || "—" }}
          <span v-if="row.cgpa" class="text-muted">· {{ row.cgpa }} CGPA</span>
        </template>

        <template #status="{ row }">
          <span
            class="badge rounded-pill"
            :class="statusBadgeClass(row.status)"
          >
            {{ formatStatus(row.status) }}
          </span>
        </template>

        <template #actions="{ row }">
          <div class="d-flex flex-wrap gap-2">
            <button
              type="button"
              class="btn btn-sm btn-outline-primary"
              @click="viewApplication(row)"
            >
              View
            </button>
            <button
              v-if="row.resume_uploaded"
              type="button"
              class="btn btn-sm btn-outline-secondary"
              :disabled="resumeLoadingId === row.application_id"
              @click="viewResume(row)"
            >
              {{
                resumeLoadingId === row.application_id ? "Opening..." : "Resume"
              }}
            </button>
          </div>
        </template>
      </DataTable>
    </template>

    <DriveFormModal
      :show="showDriveModal"
      :drive="drive"
      :start-in-edit-mode="true"
      @close="showDriveModal = false"
      @saved="onDriveSaved"
    />

    <ApplicationDetailsModal
      :show="showDetailsModal"
      :application="selectedApplication"
      @close="showDetailsModal = false"
      @saved="onActionSaved"
      @schedule="openScheduleModal"
    />

    <ScheduleInterviewModal
      :show="showScheduleModal"
      :application="selectedApplication"
      @close="showScheduleModal = false"
      @saved="onActionSaved"
    />
  </CompanyLayout>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useCompanyStore } from "@/stores/companyStore";
import { openApplicantResume } from "@/utils/resume";

import CompanyLayout from "@/layouts/CompanyLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StatCard from "@/components/shared/StatCard.vue";
import DataTable from "@/components/shared/DataTable.vue";
import DriveFormModal from "@/components/company/DriveFormModal.vue";
import ApplicationDetailsModal from "@/components/company/ApplicationDetailsModal.vue";
import ScheduleInterviewModal from "@/components/company/ScheduleInterviewModal.vue";

const route = useRoute();
const store = useCompanyStore();

const driveId = computed(() => String(route.params.id || ""));
const drive = ref(null);
const applications = ref([]);
const loading = ref(false);
const loadingApplications = ref(false);
const error = ref("");
const searchQuery = ref("");
const statusFilter = ref("");
const resumeLoadingId = ref(null);
const showDriveModal = ref(false);
const showDetailsModal = ref(false);
const showScheduleModal = ref(false);
const selectedApplication = ref(null);

const headers = [
  { key: "student_name", label: "Student" },
  { key: "department", label: "Department" },
  { key: "status", label: "Status" },
  { key: "application_date", label: "Applied On" },
  { key: "actions", label: "Actions" },
];

const loadDrive = async () => {
  if (!driveId.value) return;
  loading.value = true;
  error.value = "";
  try {
    drive.value = await store.fetchDriveById(driveId.value);
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load drive details";
  } finally {
    loading.value = false;
  }
};

const loadApplications = async () => {
  if (!driveId.value) return;
  loadingApplications.value = true;
  error.value = "";
  try {
    const data = await store.fetchDriveApplications(driveId.value);
    applications.value = (data.applications || []).map((app) => ({
      ...app,
      drive_id: driveId.value,
    }));
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load applications";
  } finally {
    loadingApplications.value = false;
  }
};

const refresh = async () => {
  await Promise.all([loadDrive(), loadApplications()]);
};

watch(
  driveId,
  async () => {
    await refresh();
  },
  { immediate: true },
);

const pipeline = computed(() => ({
  applied: applications.value.filter((app) => app.status === "applied").length,
  shortlisted: applications.value.filter((app) => app.status === "shortlisted")
    .length,
  selected: applications.value.filter((app) => app.status === "selected")
    .length,
  rejected: applications.value.filter((app) => app.status === "rejected")
    .length,
}));

const stats = computed(() => [
  {
    key: "total",
    label: "Total Applicants",
    value: applications.value.length,
    icon: "ti-users",
  },
  {
    key: "shortlisted",
    label: "Shortlisted",
    value: pipeline.value.shortlisted,
    icon: "ti-user-check",
  },
  {
    key: "selected",
    label: "Selected",
    value: pipeline.value.selected,
    icon: "ti-trophy",
  },
  {
    key: "pending",
    label: "Pending",
    value: pipeline.value.applied,
    icon: "ti-hourglass",
  },
]);

const filteredApplications = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  return applications.value.filter((app) => {
    const matchesSearch =
      !query ||
      app.student_name?.toLowerCase().includes(query) ||
      app.roll_no?.toLowerCase().includes(query) ||
      app.department?.toLowerCase().includes(query);
    const matchesStatus =
      !statusFilter.value || app.status === statusFilter.value;
    return matchesSearch && matchesStatus;
  });
});

const canEdit = computed(() => drive.value?.approval_status === "pending");

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

const formatDateTime = (value) => {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
};

const statusBadgeClass = (status) => {
  switch (status) {
    case "approved":
      return "text-bg-success";
    case "pending":
      return "text-bg-warning";
    case "closed":
      return "text-bg-secondary";
    case "rejected":
      return "text-bg-danger";
    case "applied":
      return "text-bg-secondary";
    case "shortlisted":
      return "text-bg-warning";
    case "selected":
      return "text-bg-success";
    default:
      return "text-bg-light";
  }
};

const formatStatus = (status = "") =>
  status ? status.charAt(0).toUpperCase() + status.slice(1) : "";

const openEditModal = () => {
  showDriveModal.value = true;
};

const confirmClose = () => {
  if (!drive.value) return;
  if (window.confirm(`Close the "${drive.value.job_title}" drive?`)) {
    closeDrive();
  }
};

const closeDrive = async () => {
  try {
    await store.closeDrive(driveId.value);
    await loadDrive();
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to close drive";
  }
};

const onDriveSaved = async () => {
  showDriveModal.value = false;
  await loadDrive();
  await loadApplications();
};

const viewApplication = (application) => {
  selectedApplication.value = application;
  showDetailsModal.value = true;
};

const openScheduleModal = (application) => {
  selectedApplication.value = application;
  showDetailsModal.value = false;
  showScheduleModal.value = true;
};

const onActionSaved = async () => {
  showDetailsModal.value = false;
  showScheduleModal.value = false;
  await loadApplications();
};

const viewResume = async (application) => {
  resumeLoadingId.value = application.application_id;
  try {
    await openApplicantResume(application.application_id);
  } catch (err) {
    error.value = "Failed to open resume";
  } finally {
    resumeLoadingId.value = null;
  }
};
</script>

<style scoped>
.pipeline-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  border-radius: 14px;
  background: #f8fafc;
  border: 1px solid #e9ecef;
}
</style>
