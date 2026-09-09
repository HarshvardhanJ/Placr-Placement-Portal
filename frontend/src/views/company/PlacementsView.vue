<template>
  <CompanyLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Placements"
      subtitle="Track selected candidates, joining dates, and offer letters."
    >
      <template #actions>
        <RouterLink to="/company/drives" class="btn btn-outline-primary">
          <i class="ti ti-briefcase me-2"></i>Go to Drives
        </RouterLink>
      </template>
    </PageHeader>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="row g-3 mb-4">
      <div
        v-for="stat in store.placementStats"
        :key="stat.key"
        class="col-12 col-sm-6 col-xl-3"
      >
        <StatCard :title="stat.label" :value="stat.value" :icon="stat.icon" />
      </div>
    </div>

    <div class="card shadow-sm border-0 mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-lg-4">
            <label class="form-label mb-1">Offer Letter</label>
            <select v-model="offerFilter" class="form-select">
              <option value="">All</option>
              <option value="yes">Uploaded</option>
              <option value="no">Pending</option>
            </select>
          </div>
          <div class="col-lg-4">
            <label class="form-label mb-1">Joining Window</label>
            <select v-model="joiningFilter" class="form-select">
              <option value="">All</option>
              <option value="soon">Next 7 days</option>
              <option value="later">Later</option>
            </select>
          </div>
          <div class="col-lg-4 d-flex gap-2">
            <button
              type="button"
              class="btn btn-outline-secondary flex-fill"
              @click="clearFilters"
            >
              Clear Filters
            </button>
            <button
              type="button"
              class="btn btn-outline-primary flex-fill"
              :disabled="loading"
              @click="refresh"
            >
              <i class="ti ti-refresh me-1"></i>Refresh
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="card shadow-sm p-5 text-center">
      Loading placements...
    </div>

    <DataTable
      v-else
      title="Placement Records"
      :headers="headers"
      :rows="filteredPlacements"
    >
      <template #student_name="{ row }">
        <div class="fw-semibold">{{ row.student_name }}</div>
        <small class="text-muted">{{ row.roll_no }}</small>
      </template>

      <template #job_title="{ row }">
        <div class="fw-semibold">{{ row.job_title }}</div>
      </template>

      <template #salary="{ row }">
        {{ formatCurrency(row.salary) }}
      </template>

      <template #joining_date="{ row }">
        {{ formatDate(row.joining_date) }}
      </template>

      <template #offer_letter_uploaded="{ row }">
        <span
          class="badge rounded-pill"
          :class="
            row.offer_letter_uploaded ? 'text-bg-success' : 'text-bg-secondary'
          "
        >
          {{ row.offer_letter_uploaded ? "Uploaded" : "Pending" }}
        </span>
      </template>

      <template #actions="{ row }">
        <div class="d-flex flex-wrap gap-2">
          <button
            type="button"
            class="btn btn-sm btn-outline-primary"
            @click="openEditModal(row)"
          >
            Edit
          </button>
          <button
            type="button"
            class="btn btn-sm btn-outline-secondary"
            @click="openUploadModal(row)"
          >
            Offer Letter
          </button>
          <RouterLink
            :to="`/company/drives/${row.drive_id}`"
            class="btn btn-sm btn-outline-dark"
          >
            Drive
          </RouterLink>
        </div>
      </template>
    </DataTable>

    <div
      v-if="!loading && !filteredPlacements.length"
      class="card shadow-sm p-5 text-center text-muted mt-4"
    >
      No placements match the selected filters.
    </div>

    <div v-if="showEditModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header">
            <div>
              <h5 class="modal-title mb-1">Update Placement</h5>
              <small class="text-secondary"
                >{{ selectedPlacement?.student_name }} —
                {{ selectedPlacement?.job_title }}</small
              >
            </div>
            <button
              type="button"
              class="btn-close"
              @click="closeModals"
            ></button>
          </div>
          <form @submit.prevent="savePlacement">
            <div class="modal-body">
              <div v-if="modalError" class="alert alert-danger">
                {{ modalError }}
              </div>
              <div class="mb-3">
                <label class="form-label">Salary (CTC)</label>
                <input
                  v-model.number="placementForm.salary"
                  type="number"
                  min="0"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Joining Date &amp; Time</label>
                <input
                  v-model="placementForm.joining_date"
                  type="datetime-local"
                  class="form-control"
                  required
                />
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                @click="closeModals"
              >
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? "Saving..." : "Save Changes" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="modal-backdrop fade show"></div>

    <div v-if="showUploadModal" class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header">
            <div>
              <h5 class="modal-title mb-1">Upload Offer Letter</h5>
              <small class="text-secondary">PDF only</small>
            </div>
            <button
              type="button"
              class="btn-close"
              @click="closeModals"
            ></button>
          </div>
          <form @submit.prevent="uploadOfferLetter">
            <div class="modal-body">
              <div v-if="modalError" class="alert alert-danger">
                {{ modalError }}
              </div>
              <div class="mb-3">
                <label class="form-label">Select PDF</label>
                <input
                  ref="offerFileInput"
                  type="file"
                  accept="application/pdf"
                  class="form-control"
                  required
                />
              </div>
              <p class="text-muted small mb-0">
                The file will be attached to the selected placement record.
              </p>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                @click="closeModals"
              >
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? "Uploading..." : "Upload File" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div
      v-if="showEditModal || showUploadModal"
      class="modal-backdrop fade show"
    ></div>
  </CompanyLayout>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useCompanyStore } from "@/stores/companyStore";

import CompanyLayout from "@/layouts/CompanyLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StatCard from "@/components/shared/StatCard.vue";
import DataTable from "@/components/shared/DataTable.vue";

const store = useCompanyStore();

const loading = ref(false);
const saving = ref(false);
const error = ref("");
const modalError = ref("");
const searchQuery = ref("");
const offerFilter = ref("");
const joiningFilter = ref("");
const showEditModal = ref(false);
const showUploadModal = ref(false);
const selectedPlacement = ref(null);
const offerFileInput = ref(null);

const placementForm = reactive({
  salary: null,
  joining_date: "",
});

const headers = [
  { key: "student_name", label: "Student" },
  { key: "job_title", label: "Role" },
  { key: "salary", label: "Salary" },
  { key: "joining_date", label: "Joining Date" },
  { key: "offer_letter_uploaded", label: "Offer Letter" },
  { key: "actions", label: "Actions" },
];

const loadPlacements = async () => {
  loading.value = true;
  error.value = "";
  try {
    await store.fetchPlacements(true);
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load placements";
  } finally {
    loading.value = false;
  }
};

const refresh = async () => loadPlacements();

const clearFilters = () => {
  searchQuery.value = "";
  offerFilter.value = "";
  joiningFilter.value = "";
};

const formatCurrency = (value) => {
  if (value === null || value === undefined || value === "") return "—";
  const num = Number(value);
  if (Number.isNaN(num)) return String(value);
  return `₹${num.toLocaleString("en-IN")}`;
};

const formatDate = (value) => {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString([], { dateStyle: "medium" });
};

const isJoiningSoon = (value) => {
  if (!value) return false;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return false;
  const now = new Date();
  const sevenDays = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  return date >= now && date <= sevenDays;
};

const filteredPlacements = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  return store.placements.filter((placement) => {
    const matchesSearch =
      !query ||
      placement.student_name?.toLowerCase().includes(query) ||
      placement.roll_no?.toLowerCase().includes(query) ||
      placement.job_title?.toLowerCase().includes(query);
    const matchesOffer =
      !offerFilter.value ||
      (offerFilter.value === "yes" && placement.offer_letter_uploaded) ||
      (offerFilter.value === "no" && !placement.offer_letter_uploaded);
    const matchesJoining =
      !joiningFilter.value ||
      (joiningFilter.value === "soon" &&
        isJoiningSoon(placement.joining_date)) ||
      (joiningFilter.value === "later" &&
        placement.joining_date &&
        !isJoiningSoon(placement.joining_date));

    return matchesSearch && matchesOffer && matchesJoining;
  });
});

const closeModals = () => {
  showEditModal.value = false;
  showUploadModal.value = false;
  selectedPlacement.value = null;
  modalError.value = "";
  placementForm.salary = null;
  placementForm.joining_date = "";
  if (offerFileInput.value) offerFileInput.value.value = "";
};

const openEditModal = (placement) => {
  selectedPlacement.value = placement;
  placementForm.salary = placement.salary ?? null;
  placementForm.joining_date = placement.joining_date
    ? placement.joining_date.slice(0, 16)
    : "";
  modalError.value = "";
  showUploadModal.value = false;
  showEditModal.value = true;
};

const openUploadModal = (placement) => {
  selectedPlacement.value = placement;
  modalError.value = "";
  showEditModal.value = false;
  showUploadModal.value = true;
};

const savePlacement = async () => {
  if (!selectedPlacement.value) return;
  saving.value = true;
  modalError.value = "";
  try {
    await store.updatePlacement(selectedPlacement.value.placement_id, {
      salary: placementForm.salary,
      joining_date: placementForm.joining_date,
    });
    closeModals();
    await loadPlacements();
  } catch (err) {
    modalError.value =
      err?.response?.data?.error || "Failed to update placement";
  } finally {
    saving.value = false;
  }
};

const uploadOfferLetter = async () => {
  if (!selectedPlacement.value) return;
  const file = offerFileInput.value?.files?.[0];
  if (!file) {
    modalError.value = "Please select a PDF file.";
    return;
  }
  saving.value = true;
  modalError.value = "";
  try {
    await store.uploadOfferLetter(selectedPlacement.value.placement_id, file);
    closeModals();
    await loadPlacements();
  } catch (err) {
    modalError.value =
      err?.response?.data?.error || "Failed to upload offer letter";
  } finally {
    saving.value = false;
  }
};

onMounted(async () => {
  await loadPlacements();
});
</script>
