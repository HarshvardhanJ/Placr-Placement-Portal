<template>
  <CompanyLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Applications"
      subtitle="Review applicants drive by drive, shortlist, and schedule interviews."
    />

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="card shadow-sm border-0 mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-center">
          <div class="col-lg-5">
            <label class="form-label mb-1">Drive</label>
            <select v-model="selectedDriveId" class="form-select">
              <option value="" disabled>Select a drive</option>
              <option
                v-for="drive in drives"
                :key="drive.drive_id"
                :value="drive.drive_id"
              >
                {{ drive.job_title }} ({{
                  formatStatus(drive.approval_status)
                }})
              </option>
            </select>
          </div>

          <div class="col-lg-3">
            <label class="form-label mb-1">Status</label>
            <select v-model="statusFilter" class="form-select">
              <option value="">All Statuses</option>
              <option value="applied">Applied</option>
              <option value="shortlisted">Shortlisted</option>
              <option value="selected">Selected</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          <div class="col-lg-2">
            <label class="form-label mb-1 d-block">&nbsp;</label>
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

    <div
      v-if="!drives.length && !loadingDrives"
      class="card shadow-sm p-5 text-center text-muted"
    >
      No approved drives yet. Once admin approves a drive, applicants will show
      up here.
    </div>

    <template v-else-if="selectedDriveId">
      <div class="row g-3 mb-4">
        <div
          v-for="stat in stats"
          :key="stat.title"
          class="col-12 col-sm-6 col-xl-3"
        >
          <StatCard :title="stat.title" :value="stat.value" />
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
        <template #student="{ row }">
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
              class="btn btn-sm btn-outline-primary"
              @click="viewApplication(row)"
            >
              View
            </button>
            <button
              v-if="row.resume_uploaded"
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
import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";
import { openApplicantResume } from "@/utils/resume";

import CompanyLayout from "@/layouts/CompanyLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StatCard from "@/components/shared/StatCard.vue";
import DataTable from "@/components/shared/DataTable.vue";
import ApplicationDetailsModal from "@/components/company/ApplicationDetailsModal.vue";
import ScheduleInterviewModal from "@/components/company/ScheduleInterviewModal.vue";

const route = useRoute();
const router = useRouter();

const searchQuery = ref("");
const statusFilter = ref("");
const error = ref("");

const drives = ref([]);
const loadingDrives = ref(false);
const selectedDriveId = ref("");

const applications = ref([]);
const loadingApplications = ref(false);

const showDetailsModal = ref(false);
const showScheduleModal = ref(false);
const selectedApplication = ref(null);
const resumeLoadingId = ref(null);
const pendingDeepLinkDriveId = route.query.drive || "";
const pendingDeepLinkApplicationId = ref(route.query.application || "");

const headers = [
  { key: "student", label: "Student" },
  { key: "department", label: "Department" },
  { key: "status", label: "Status" },
  { key: "application_date", label: "Applied On" },
  { key: "actions", label: "Actions" },
];

const loadDrives = async () => {
  loadingDrives.value = true;
  error.value = "";
  try {
    const { data } = await api.get("/company/drives");
    drives.value = data.drives
      .filter(
        (d) =>
          d.approval_status === "approved" || d.approval_status === "closed",
      )
      .sort((a, b) =>
        a.approval_status === b.approval_status
          ? 0
          : a.approval_status === "approved"
            ? -1
            : 1,
      );

    const queryDrive = pendingDeepLinkDriveId;
    if (queryDrive && drives.value.some((d) => d.drive_id === queryDrive)) {
      selectedDriveId.value = queryDrive;
    } else if (drives.value.length) {
      selectedDriveId.value = drives.value[0].drive_id;
    }
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load drives";
  } finally {
    loadingDrives.value = false;
  }
};

const loadApplications = async (driveId) => {
  if (!driveId) return;
  loadingApplications.value = true;
  error.value = "";
  try {
    const { data } = await api.get(`/company/drives/${driveId}/applications`);
    applications.value = data.applications.map((app) => ({
      ...app,
      drive_id: driveId,
    }));

    if (pendingDeepLinkApplicationId.value) {
      const match = applications.value.find(
        (a) => a.application_id === pendingDeepLinkApplicationId.value,
      );
      if (match) viewApplication(match);
      pendingDeepLinkApplicationId.value = "";
    }
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load applications";
  } finally {
    loadingApplications.value = false;
  }
};

watch(selectedDriveId, (driveId) => {
  applications.value = [];
  if (driveId) loadApplications(driveId);
});

const stats = computed(() => [
  { title: "Total", value: applications.value.length },
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

const filteredApplications = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  return applications.value.filter((app) => {
    const matchesSearch =
      !query ||
      app.student_name?.toLowerCase().includes(query) ||
      app.roll_no?.toLowerCase().includes(query);
    const matchesStatus =
      !statusFilter.value || app.status === statusFilter.value;
    return matchesSearch && matchesStatus;
  });
});

const clearFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
};

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

const formatStatus = (status = "") =>
  status ? status.charAt(0).toUpperCase() + status.slice(1) : "";

const viewApplication = (application) => {
  selectedApplication.value = application;
  showDetailsModal.value = true;
};

const openScheduleModal = (application) => {
  selectedApplication.value = application;
  showDetailsModal.value = false;
  showScheduleModal.value = true;
};

const onActionSaved = () => {
  showDetailsModal.value = false;
  showScheduleModal.value = false;
  loadApplications(selectedDriveId.value);
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

onMounted(() => {
  loadDrives();
  router.replace({ path: "/company/applications" });
});
</script>
