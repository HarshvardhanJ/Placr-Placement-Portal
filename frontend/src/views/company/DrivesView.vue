<template>
  <CompanyLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Jobs & Drives"
      subtitle="Create and manage your placement drives."
    >
      <template #actions>
        <button
          type="button"
          class="btn btn-primary d-inline-flex align-items-center gap-2"
          @click="openCreateModal"
        >
          <i class="ti ti-plus"></i>
          <span>Create Drive</span>
        </button>
      </template>
    </PageHeader>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

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
          <div class="col-lg-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
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

    <div v-if="loading" class="card shadow-sm p-5 text-center">
      Loading drives...
    </div>

    <DataTable v-else title="Drives" :headers="headers" :rows="filteredDrives">
      <template #job_title="{ row }">
        <div class="fw-semibold">{{ row.job_title }}</div>
        <small class="text-muted">{{
          row.job_location || "Location not set"
        }}</small>
      </template>

      <template #applicants="{ row }">
        <span>{{ row.applicants }}</span>
      </template>

      <template #deadline="{ row }">
        {{ row.deadline }}
      </template>

      <template #status="{ row }">
        <span
          class="badge rounded-pill"
          :class="statusBadgeClass(row.approval_status)"
        >
          {{ formatStatus(row.approval_status) }}
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
            v-if="row.approval_status === 'pending'"
            class="btn btn-sm btn-outline-secondary"
            @click="editDrive(row)"
          >
            Edit
          </button>

          <RouterLink
            :to="`/company/applications?drive=${row.drive_id}`"
            class="btn btn-sm btn-outline-primary"
          >
            Applicants
          </RouterLink>

          <button
            v-if="row.approval_status === 'approved'"
            class="btn btn-sm btn-outline-warning"
            @click="confirmClose(row)"
          >
            Close
          </button>
        </div>
      </template>
    </DataTable>

    <DriveFormModal
      :show="showModal"
      :drive="selectedDrive"
      :start-in-edit-mode="modalEditMode"
      @close="showModal = false"
      @saved="onSaved"
    />
  </CompanyLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";

import CompanyLayout from "@/layouts/CompanyLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StatCard from "@/components/shared/StatCard.vue";
import DataTable from "@/components/shared/DataTable.vue";
import DriveFormModal from "@/components/company/DriveFormModal.vue";

const route = useRoute();
const router = useRouter();

const searchQuery = ref("");
const statusFilter = ref("");
const loading = ref(false);
const error = ref("");
const drives = ref([]);

const showModal = ref(false);
const selectedDrive = ref(null);
const modalEditMode = ref(false);

const headers = [
  { key: "job_title", label: "Role" },
  { key: "applicants", label: "Applicants" },
  { key: "deadline", label: "Deadline" },
  { key: "status", label: "Status" },
  { key: "actions", label: "Actions" },
];

const loadDrives = async () => {
  loading.value = true;
  error.value = "";
  try {
    const { data } = await api.get("/company/drives");
    drives.value = data.drives.map((drive) => ({
      ...drive,
      deadline: new Date(drive.application_deadline).toLocaleDateString(),
    }));
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load drives";
  } finally {
    loading.value = false;
  }
};

const stats = computed(() => [
  { title: "Total Drives", value: drives.value.length },
  {
    title: "Approved",
    value: drives.value.filter((d) => d.approval_status === "approved").length,
  },
  {
    title: "Pending",
    value: drives.value.filter((d) => d.approval_status === "pending").length,
  },
  {
    title: "Closed",
    value: drives.value.filter((d) => d.approval_status === "closed").length,
  },
]);

const filteredDrives = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  return drives.value.filter((drive) => {
    const matchesSearch =
      !query ||
      drive.job_title?.toLowerCase().includes(query) ||
      drive.job_location?.toLowerCase().includes(query);
    const matchesStatus =
      !statusFilter.value || drive.approval_status === statusFilter.value;
    return matchesSearch && matchesStatus;
  });
});

const clearFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
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
    default:
      return "text-bg-light";
  }
};

const formatStatus = (status = "") =>
  status.charAt(0).toUpperCase() + status.slice(1);

const openCreateModal = () => {
  selectedDrive.value = null;
  modalEditMode.value = false;
  showModal.value = true;
};

const viewDrive = (drive) => {
  router.push(`/company/drives/${drive.drive_id}`);
};

const editDrive = (drive) => {
  selectedDrive.value = drive;
  modalEditMode.value = true;
  showModal.value = true;
};

const onSaved = () => {
  showModal.value = false;
  loadDrives();
};

const confirmClose = (drive) => {
  if (
    window.confirm(
      `Close the "${drive.job_title}" drive? This cannot be undone.`,
    )
  ) {
    closeDrive(drive);
  }
};

const closeDrive = async (drive) => {
  try {
    await api.put(`/company/drives/${drive.drive_id}/close`);
    drive.approval_status = "closed";
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to close drive";
  }
};

onMounted(() => {
  loadDrives();
  if (route.query.new === "1") {
    openCreateModal();
    router.replace({ path: "/company/drives" });
  }
});
</script>
