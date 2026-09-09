<template>
  <div class="dashboard-section">
    <div class="section-hero card shadow-sm border-0 mb-4">
      <div
        class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
      >
        <div>
          <span class="hero-kicker">Reports</span>
          <h3 class="fw-bold mb-2">Your documents and placement records</h3>
          <p class="text-muted mb-0">
            Review resume status, application history, and placement
            confirmations.
          </p>
        </div>

        <button
          class="btn btn-primary"
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
    </div>

    <div v-if="exportMessage" class="alert" :class="exportAlertClass">
      {{ exportMessage }}
    </div>

    <div class="row g-3 mb-4">
      <div
        v-for="card in reportCards"
        :key="card.label"
        class="col-12 col-md-4"
      >
        <div class="report-card card shadow-sm border-0 h-100">
          <div class="card-body p-4">
            <div class="d-flex align-items-start justify-content-between">
              <div>
                <div class="text-muted small mb-1">{{ card.label }}</div>
                <div
                  class="report-value"
                  :class="{ muted: card.value === 'Missing' }"
                >
                  {{ card.value }}
                </div>
              </div>
              <div class="report-badge">
                <i :class="['ti', card.icon]"></i>
              </div>
            </div>
            <small class="text-muted d-block mt-2">{{ card.caption }}</small>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm border-0">
      <div class="card-body p-4">
        <div
          class="d-flex align-items-start justify-content-between gap-3 mb-4"
        >
          <div>
            <h6 class="fw-semibold mb-1">Quick actions</h6>
            <small class="text-muted"
              >Jump to the places you will use most often</small
            >
          </div>
          <span class="pill-label">Student</span>
        </div>

        <div class="d-flex flex-wrap gap-2">
          <RouterLink
            to="/student/profile"
            class="btn btn-outline-primary btn-sm"
          >
            Update Profile
          </RouterLink>
          <RouterLink
            to="/student/drives"
            class="btn btn-outline-secondary btn-sm"
          >
            View Drives
          </RouterLink>
          <RouterLink
            to="/student/applications"
            class="btn btn-outline-secondary btn-sm"
          >
            View Applications
          </RouterLink>
          <RouterLink
            to="/student/placements"
            class="btn btn-outline-secondary btn-sm"
          >
            View Placements
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from "vue";
import { storeToRefs } from "pinia";
import { useStudentStore } from "@/stores/studentStore";

const store = useStudentStore();
const { reportCards } = storeToRefs(store);
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
.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.section-hero {
  border-radius: 1rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #0d6efd;
  margin-bottom: 0.35rem;
}

.report-card {
  border-radius: 1rem;
  background: #fff;
}

.report-value {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  line-height: 1.1;
}

.report-value.muted {
  color: #6b7280;
}

.report-badge {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: #eef4ff;
  color: #0d6efd;
  display: grid;
  place-items: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.pill-label {
  display: inline-flex;
  align-items: center;
  padding: 0.38rem 0.7rem;
  border-radius: 999px;
  background: #eef4ff;
  color: #0d6efd;
  font-size: 0.78rem;
  font-weight: 700;
}
</style>
