<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <div class="d-flex align-items-start justify-content-between gap-3 mb-4">
        <div>
          <h6 class="mb-1 fw-semibold">Analytics Snapshot</h6>
          <small class="text-muted"
            >Drive activity, funnel progress, and placement summary.</small
          >
        </div>
        <RouterLink
          to="/company/placements"
          class="btn btn-outline-primary btn-sm"
        >
          <i class="ti ti-trophy me-1"></i>Placements
        </RouterLink>
      </div>

      <div class="row g-3 mb-4">
        <div
          v-for="card in cards"
          :key="card.label"
          class="col-12 col-md-6 col-xl-3"
        >
          <div class="metric-card border rounded-4 p-3 h-100">
            <div class="text-muted small mb-1">{{ card.label }}</div>
            <div class="fw-bold fs-4">{{ card.value }}</div>
            <small class="text-muted">{{ card.delta }}</small>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-12 col-lg-7">
          <div class="p-3 border rounded-4 h-100">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h6 class="fw-semibold mb-0">Application Funnel</h6>
              <small class="text-muted">From current dashboard totals</small>
            </div>

            <template v-if="hasFunnelData">
              <div v-for="item in funnel" :key="item.label" class="mb-3">
                <div class="d-flex justify-content-between small mb-1">
                  <span>{{ item.label }}</span>
                  <span class="text-muted">{{ item.value }}</span>
                </div>
                <div class="progress funnel-progress">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    :style="{ width: `${item.width}%` }"
                    :aria-valuenow="item.value"
                    aria-valuemin="0"
                    :aria-valuemax="funnelMax"
                  ></div>
                </div>
              </div>
            </template>

            <div v-else class="empty-state">
              <i class="ti ti-chart-bar-off empty-icon"></i>
              <div class="fw-semibold mb-1">No application data yet</div>
              <small class="text-muted"
                >Once students start applying, the funnel will appear
                here.</small
              >
            </div>
          </div>
        </div>

        <div class="col-12 col-lg-5">
          <div class="p-3 border rounded-4 h-100">
            <h6 class="fw-semibold mb-3">Drive Status Mix</h6>

            <template v-if="hasDriveData">
              <div
                v-for="item in driveBreakdown"
                :key="item.label"
                class="mb-3"
              >
                <div class="d-flex justify-content-between small mb-1">
                  <span>{{ item.label }}</span>
                  <span class="text-muted">{{ item.count }}</span>
                </div>
                <div class="progress status-progress">
                  <div
                    class="progress-bar"
                    :class="item.barClass"
                    role="progressbar"
                    :style="{ width: `${item.width}%` }"
                    :aria-valuenow="item.count"
                    aria-valuemin="0"
                    :aria-valuemax="driveTotal"
                  ></div>
                </div>
              </div>

              <div class="pt-2 border-top mt-3">
                <small class="text-muted">
                  Open drives: {{ openDrives }} · Pending approval:
                  {{ pendingDrives }} · Closed: {{ closedDrives }}
                </small>
              </div>
            </template>

            <div v-else class="empty-state">
              <i class="ti ti-briefcase-off empty-icon"></i>
              <div class="fw-semibold mb-1">No drive data yet</div>
              <small class="text-muted"
                >Create a drive to see status distribution here.</small
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useCompanyStore } from "@/stores/companyStore";

const store = useCompanyStore();
const { dashboard } = storeToRefs(store);

const stats = computed(() => dashboard.value?.stats || {});
const drives = computed(() => dashboard.value?.active_drives || []);

const cards = computed(() => [
  {
    label: "Total Applications",
    value: Number(stats.value.total_applications || 0),
    delta: "All drives combined",
  },
  {
    label: "Interviews Scheduled",
    value: Number(stats.value.interviews_scheduled || 0),
    delta: "Upcoming slots",
  },
  {
    label: "Offers Made",
    value: Number(stats.value.offers_made || 0),
    delta: "Candidates selected",
  },
  {
    label: "Active Drives",
    value: Number(stats.value.active_drives || 0),
    delta: "Currently open",
  },
]);

const totalApplications = computed(() =>
  Number(stats.value.total_applications || 0),
);
const funnelMax = computed(() => Math.max(totalApplications.value, 1));
const hasFunnelData = computed(() => totalApplications.value > 0);

const clampPercent = (value) => {
  if (!Number.isFinite(value) || value <= 0) return 0;
  return Math.min(100, Math.max(0, value));
};

const funnel = computed(() => {
  const total = totalApplications.value;
  if (!total) {
    return [
      { label: "Applied", value: 0, width: 0 },
      { label: "Shortlisted", value: 0, width: 0 },
      { label: "Selected", value: 0, width: 0 },
    ];
  }

  const shortlisted = Number(stats.value.interviews_scheduled || 0);
  const selected = Number(stats.value.offers_made || 0);

  return [
    {
      label: "Applied",
      value: total,
      width: 100,
    },
    {
      label: "Shortlisted",
      value: shortlisted,
      width: clampPercent((shortlisted / total) * 100),
    },
    {
      label: "Selected",
      value: selected,
      width: clampPercent((selected / total) * 100),
    },
  ];
});

const driveTotal = computed(() => Math.max(drives.value.length, 1));
const hasDriveData = computed(() => drives.value.length > 0);

const driveBreakdown = computed(() => {
  const active = drives.value.filter(
    (drive) => drive.status === "active",
  ).length;
  const interviewing = drives.value.filter(
    (drive) => drive.status === "interviewing",
  ).length;
  const shortlisting = drives.value.filter(
    (drive) => drive.status === "shortlisting",
  ).length;

  return [
    {
      label: "Active",
      count: active,
      width: clampPercent((active / driveTotal.value) * 100),
      barClass: "bg-primary",
    },
    {
      label: "Interviewing",
      count: interviewing,
      width: clampPercent((interviewing / driveTotal.value) * 100),
      barClass: "bg-info",
    },
    {
      label: "Shortlisting",
      count: shortlisting,
      width: clampPercent((shortlisting / driveTotal.value) * 100),
      barClass: "bg-warning",
    },
  ];
});

const openDrives = computed(
  () => drives.value.filter((drive) => drive.status === "active").length,
);
const pendingDrives = computed(
  () => drives.value.filter((drive) => drive.status === "shortlisting").length,
);
const closedDrives = computed(
  () => drives.value.filter((drive) => drive.status === "closed").length,
);
</script>

<style scoped>
.metric-card {
  background: #fff;
}

.funnel-progress,
.status-progress {
  background-color: #e9ecef;
}

.empty-state {
  min-height: 220px;
  display: grid;
  place-items: center;
  text-align: center;
  padding: 2rem 1rem;
  border: 1px dashed #d9dee7;
  border-radius: 1rem;
  background: #fafbff;
}

.empty-icon {
  font-size: 2rem;
  color: #8a94a6;
  margin-bottom: 0.5rem;
}
</style>
