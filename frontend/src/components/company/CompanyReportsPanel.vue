<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <div class="d-flex align-items-start justify-content-between gap-3 mb-4">
        <div>
          <h6 class="mb-1 fw-semibold">Reports</h6>
          <small class="text-muted">Download-ready summary cards for your placement team.</small>
        </div>
        <button
          class="btn btn-primary btn-sm"
          type="button"
          :disabled="exportBusy"
          @click="startExport"
        >
          <span
            v-if="exportBusy"
            class="spinner-border spinner-border-sm me-2"
            aria-hidden="true"
          ></span>
          <i v-else class="ti ti-download me-2"></i>{{ exportButtonText }}
        </button>
      </div>

      <div v-if="exportMessage" class="alert mb-4" :class="exportAlertClass">
        {{ exportMessage }}
      </div>

      <div class="row g-3 mb-4">
        <div v-for="card in reportCards" :key="card.label" class="col-12 col-md-4">
          <div class="report-tile border rounded-4 p-3 h-100">
            <div class="fw-semibold">{{ card.label }}</div>
            <div class="display-6 fw-bold my-2">{{ card.value }}</div>
            <small class="text-muted">{{ card.caption }}</small>
          </div>
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2">
        <RouterLink to="/company/placements" class="btn btn-outline-primary btn-sm">
          View Placements
        </RouterLink>
        <RouterLink to="/company/applications" class="btn btn-outline-secondary btn-sm">
          Review Applications
        </RouterLink>
        <RouterLink to="/company/interviews" class="btn btn-outline-secondary btn-sm">
          Interview Schedule
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from "vue";
import { storeToRefs } from "pinia";
import { useCompanyStore } from "@/stores/companyStore";

const store = useCompanyStore();
const { placements, dashboard } = storeToRefs(store);
const exportTaskId = ref("");
const exportState = ref("");
const exportMessage = ref("");
const exportError = ref(false);
const exportStartedAt = ref(0);
let pollTimer = null;
const EXPORT_POLL_TIMEOUT_MS = 120000;

const exportBusy = computed(() =>
  ["PENDING", "STARTED", "RETRY"].includes(exportState.value),
);

const exportButtonText = computed(() =>
  exportBusy.value ? "Preparing CSV" : "Export CSV",
);

const exportAlertClass = computed(() =>
  exportError.value ? "alert-danger" : "alert-info",
);

const reportCards = computed(() => {
  const totalPlacements = placements.value?.length || 0;
  const offersMade = dashboard.value?.stats?.offers_made || 0;
  const totalApplications = dashboard.value?.stats?.total_applications || 0;

  return [
    {
      label: "Applications",
      value: totalApplications,
      caption: "Across all company drives",
    },
    {
      label: "Offers",
      value: offersMade,
      caption: "Candidates selected so far",
    },
    {
      label: "Placements",
      value: totalPlacements,
      caption: "Confirmed placement records",
    },
  ];
});

const saveBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
};

const stopPolling = () => {
  if (pollTimer) {
    window.clearTimeout(pollTimer);
    pollTimer = null;
  }
};

const downloadReadyExport = async (result) => {
  const filename = result?.filename;
  if (!filename) {
    throw new Error("Export completed without a filename");
  }

  const response = await store.downloadExport(filename);
  saveBlob(response.data, filename);
};

const pollExportStatus = async () => {
  if (!exportTaskId.value) return;

  try {
    if (
      exportStartedAt.value &&
      Date.now() - exportStartedAt.value > EXPORT_POLL_TIMEOUT_MS
    ) {
      stopPolling();
      exportError.value = true;
      exportState.value = "";
      exportMessage.value =
        "CSV export is taking longer than expected. Please try again in a moment.";
      return;
    }

    const status = await store.getExportStatus(exportTaskId.value);
    exportState.value = status.state;

    if (status.state === "SUCCESS") {
      stopPolling();
      const result = status.result || {};
      if (result.success === false) {
        exportError.value = true;
        exportMessage.value = result.error || result.reason || "Export failed.";
        return;
      }
      await downloadReadyExport(result);
      exportError.value = false;
      exportMessage.value = "CSV export is ready and has been downloaded.";
      exportState.value = "";
      exportStartedAt.value = 0;
      return;
    }

    if (status.state === "FAILURE") {
      stopPolling();
      exportError.value = true;
      exportMessage.value = "Export job failed. Please try again.";
      exportState.value = "";
      exportStartedAt.value = 0;
      return;
    }

    exportMessage.value = "CSV export is being prepared. You will also receive an email when it is ready.";
    pollTimer = window.setTimeout(pollExportStatus, 2500);
  } catch (error) {
    stopPolling();
    exportError.value = true;
    exportState.value = "";
    exportStartedAt.value = 0;
    exportMessage.value =
      error?.response?.data?.error || error?.message || "Failed to check export status.";
  }
};

const startExport = async () => {
  stopPolling();
  exportError.value = false;
  exportState.value = "PENDING";
  exportStartedAt.value = Date.now();
  exportMessage.value = "Starting CSV export...";

  try {
    const data = await store.startExport();
    exportTaskId.value = data.task_id;
    exportMessage.value = data.message || "CSV export started.";
    await pollExportStatus();
  } catch (error) {
    exportError.value = true;
    exportState.value = "";
    exportStartedAt.value = 0;
    exportMessage.value =
      error?.response?.data?.error || error?.message || "Failed to start export.";
  }
};

onBeforeUnmount(stopPolling);
</script>

<style scoped>
.report-tile {
  background: #fff;
}
</style>
