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
              <BaseChart
                type="bar"
                :data="funnelChartData"
                :options="barChartOptions"
                :height="360"
                aria-label="Company application funnel chart"
              />
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
              <BaseChart
                type="doughnut"
                :data="driveChartData"
                :options="doughnutChartOptions"
                :height="320"
                aria-label="Company drive status mix chart"
              />

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
import BaseChart from "@/components/shared/BaseChart.vue";

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
const hasFunnelData = computed(() => totalApplications.value > 0);

const funnel = computed(() => {
  const shortlisted = Number(stats.value.interviews_scheduled || 0);
  const selected = Number(stats.value.offers_made || 0);

  return [
    {
      label: "Applied",
      value: totalApplications.value,
    },
    {
      label: "Shortlisted",
      value: shortlisted,
    },
    {
      label: "Selected",
      value: selected,
    },
  ];
});

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
    },
    {
      label: "Interviewing",
      count: interviewing,
    },
    {
      label: "Shortlisting",
      count: shortlisting,
    },
  ];
});

const funnelChartData = computed(() => ({
  labels: funnel.value.map((item) => item.label),
  datasets: [
    {
      label: "Candidates",
      data: funnel.value.map((item) => item.value),
      backgroundColor: ["#2563eb", "#06b6d4", "#10b981"],
      borderRadius: 8,
      maxBarThickness: 54,
    },
  ],
}));

const driveChartData = computed(() => ({
  labels: driveBreakdown.value.map((item) => item.label),
  datasets: [
    {
      data: driveBreakdown.value.map((item) => item.count),
      backgroundColor: ["#2563eb", "#06b6d4", "#f59e0b"],
      borderColor: "#ffffff",
      borderWidth: 4,
      hoverOffset: 6,
    },
  ],
}));

const barChartOptions = {
  plugins: {
    legend: { display: false },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { precision: 0 },
      grid: { color: "#eef2f7" },
    },
    x: {
      grid: { display: false },
    },
  },
};

const doughnutChartOptions = {
  cutout: "62%",
  plugins: {
    legend: {
      position: "bottom",
      labels: { usePointStyle: true, boxWidth: 8 },
    },
  },
};

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
