<template>
  <div class="dashboard-section">
    <div class="section-hero card shadow-sm border-0 mb-4">
      <div
        class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
      >
        <div>
          <span class="hero-kicker">Analytics</span>
          <h3 class="fw-bold mb-2">Your application progress at a glance</h3>
          <p class="text-muted mb-0">
            Track applications, shortlist movement, and placement outcomes in
            one place.
          </p>
        </div>

        <RouterLink to="/student/placements" class="btn btn-outline-primary">
          <i class="ti ti-trophy me-2"></i>View Placements
        </RouterLink>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div
        v-for="card in cards"
        :key="card.label"
        class="col-12 col-md-6 col-xl-3"
      >
        <div class="metric-card card shadow-sm border-0 h-100">
          <div class="card-body p-3">
            <div class="text-muted small mb-1">{{ card.label }}</div>
            <div class="d-flex align-items-end justify-content-between">
              <div class="fw-bold fs-3">{{ card.value }}</div>
              <div class="metric-icon">
                <i :class="['ti', card.icon]"></i>
              </div>
            </div>
            <small class="text-muted d-block mt-1">{{ card.delta }}</small>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12 col-lg-7">
        <div class="panel-card card shadow-sm border-0 h-100">
          <div class="card-body p-4">
            <div
              class="d-flex align-items-start justify-content-between gap-3 mb-4"
            >
              <div>
                <h6 class="fw-semibold mb-1">Application Funnel</h6>
                <small class="text-muted">From your dashboard totals</small>
              </div>
              <span class="pill-label">Overview</span>
            </div>

            <template v-if="hasFunnelData">
              <BaseChart
                type="bar"
                :data="funnelChartData"
                :options="barChartOptions"
                aria-label="Student application funnel chart"
              />
            </template>

            <StudentEmptyState
              v-else
              icon="ti-chart-bar-off"
              title="No application data yet"
              subtitle="Apply to your first drive to see analytics here."
            />
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-5">
        <div class="panel-card card shadow-sm border-0 h-100">
          <div class="card-body p-4">
            <div
              class="d-flex align-items-start justify-content-between gap-3 mb-4"
            >
              <div>
                <h6 class="fw-semibold mb-1">Status Mix</h6>
                <small class="text-muted">Application progress breakdown</small>
              </div>
              <span class="pill-label">Live</span>
            </div>

            <template v-if="hasStatusData">
              <BaseChart
                type="doughnut"
                :data="statusChartData"
                :options="doughnutChartOptions"
                aria-label="Student application status mix chart"
              />

              <div class="pt-3 border-top mt-3">
                <div class="d-flex flex-wrap gap-3 small text-muted">
                  <span
                    >Applied:
                    <strong class="text-dark">{{ appliedCount }}</strong></span
                  >
                  <span
                    >Shortlisted:
                    <strong class="text-dark">{{
                      shortlistedCount
                    }}</strong></span
                  >
                  <span
                    >Selected:
                    <strong class="text-dark">{{ selectedCount }}</strong></span
                  >
                </div>
              </div>
            </template>

            <StudentEmptyState
              v-else
              icon="ti-badge-off"
              title="No status data yet"
              subtitle="Status breakdown will appear once your applications move forward."
            />
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm border-0 mt-4">
      <div class="card-body p-4">
        <div class="d-flex align-items-center justify-content-between mb-3">
          <div>
            <h6 class="fw-semibold mb-1">Quick insights</h6>
            <small class="text-muted"
              >A compact summary of your current progress</small
            >
          </div>
        </div>

        <div class="row g-3">
          <div class="col-12 col-md-4">
            <div class="insight-box">
              <div class="insight-title">Applications</div>
              <div class="insight-value">{{ appliedCount }}</div>
              <small class="text-muted">Submitted across drives</small>
            </div>
          </div>
          <div class="col-12 col-md-4">
            <div class="insight-box">
              <div class="insight-title">Shortlisted</div>
              <div class="insight-value">{{ shortlistedCount }}</div>
              <small class="text-muted">Awaiting interviews</small>
            </div>
          </div>
          <div class="col-12 col-md-4">
            <div class="insight-box">
              <div class="insight-title">Selected</div>
              <div class="insight-value">{{ selectedCount }}</div>
              <small class="text-muted">Offers received</small>
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
import { useStudentStore } from "@/stores/studentStore";
import BaseChart from "@/components/shared/BaseChart.vue";
import StudentEmptyState from "./StudentEmptyState.vue";

const store = useStudentStore();
const { dashboard } = storeToRefs(store);

const counts = computed(() => dashboard.value?.counts || {});

const appliedCount = computed(() => Number(counts.value.applied || 0));
const shortlistedCount = computed(() => Number(counts.value.shortlisted || 0));
const selectedCount = computed(() => Number(counts.value.selected || 0));
const eligibleCount = computed(() => Number(counts.value.eligible || 0));

const cards = computed(() => [
  {
    label: "Applications",
    value: appliedCount.value,
    delta: "Submitted drives",
    icon: "ti-send",
  },
  {
    label: "Shortlisted",
    value: shortlistedCount.value,
    delta: "Interview stage",
    icon: "ti-star",
  },
  {
    label: "Selected",
    value: selectedCount.value,
    delta: "Offers received",
    icon: "ti-trophy",
  },
  {
    label: "Eligible",
    value: eligibleCount.value,
    delta: "Recommended drives",
    icon: "ti-briefcase",
  },
]);

const totalApplications = computed(() => appliedCount.value);
const hasFunnelData = computed(() => totalApplications.value > 0);
const hasStatusData = computed(
  () =>
    appliedCount.value > 0 ||
    shortlistedCount.value > 0 ||
    selectedCount.value > 0,
);

const funnel = computed(() => {
  return [
    { label: "Applied", value: totalApplications.value },
    { label: "Shortlisted", value: shortlistedCount.value },
    { label: "Selected", value: selectedCount.value },
  ];
});

const funnelChartData = computed(() => ({
  labels: funnel.value.map((item) => item.label),
  datasets: [
    {
      label: "Applications",
      data: funnel.value.map((item) => item.value),
      backgroundColor: ["#2563eb", "#f59e0b", "#10b981"],
      borderRadius: 8,
      maxBarThickness: 54,
    },
  ],
}));

const statusChartData = computed(() => ({
  labels: ["Applied", "Shortlisted", "Selected"],
  datasets: [
    {
      data: [appliedCount.value, shortlistedCount.value, selectedCount.value],
      backgroundColor: ["#2563eb", "#f59e0b", "#10b981"],
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

.metric-card,
.panel-card,
.insight-box {
  background: #fff;
  border-radius: 1rem;
}

.metric-icon {
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

.progress-soft {
  height: 10px;
  background-color: #e9ecef;
}

.insight-box {
  border: 1px solid #e9ecef;
  padding: 1rem;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.03);
  height: 100%;
}

.insight-title {
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #6b7280;
}

.insight-value {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  line-height: 1.1;
  margin: 0.35rem 0;
}
</style>
