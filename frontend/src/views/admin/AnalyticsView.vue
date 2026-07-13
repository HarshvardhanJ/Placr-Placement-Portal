<template>
  <DashboardLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Analytics"
      subtitle="Placement trends, funnel metrics, and activity snapshots."
    >
      <template #actions>
        <RouterLink to="/admin/reports" class="btn btn-outline-primary">
          <i class="ti ti-report-analytics me-2"></i>Reports
        </RouterLink>
      </template>
    </PageHeader>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="row g-3 mb-4">
      <div
        class="col-12 col-lg-4"
        v-for="item in filteredCards"
        :key="item.title"
      >
        <div class="mini-panel shadow-sm">
          <div class="text-secondary small text-uppercase fw-semibold mb-1">
            {{ item.title }}
          </div>
          <div class="fw-bold fs-3">{{ item.value }}</div>
          <small class="text-secondary">{{ item.note }}</small>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12 col-xl-8">
        <div class="analytics-panel card shadow-sm border-0 h-100">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between gap-3 mb-4">
              <div>
                <h6 class="fw-semibold mb-1">Placement Trends</h6>
                <small class="text-muted">Applications and placements over the last six months</small>
              </div>
              <span class="pill-label">Monthly</span>
            </div>
            <BaseChart
              type="line"
              :data="monthlyChartData"
              :options="lineChartOptions"
              aria-label="Monthly placement and application trend chart"
            />
          </div>
        </div>
      </div>

      <div class="col-12 col-xl-4">
        <div class="analytics-panel card shadow-sm border-0 h-100">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between gap-3 mb-4">
              <div>
                <h6 class="fw-semibold mb-1">Application Funnel</h6>
                <small class="text-muted">Current application statuses</small>
              </div>
              <span class="pill-label">Live</span>
            </div>
            <BaseChart
              type="doughnut"
              :data="funnelChartData"
              :options="doughnutChartOptions"
              aria-label="Admin application funnel chart"
            />
          </div>
        </div>
      </div>

      <div class="col-12">
        <div class="analytics-panel card shadow-sm border-0">
          <div class="card-body p-4">
            <div class="d-flex flex-column flex-md-row justify-content-between gap-3 mb-4">
              <div>
                <h6 class="fw-semibold mb-1">Job Demand by Skills</h6>
                <small class="text-muted">Most requested skills from active and historical drives</small>
              </div>
              <span class="pill-label">Top {{ skillDemand.length || 0 }}</span>
            </div>
            <BaseChart
              v-if="skillDemand.length"
              type="bar"
              :data="skillChartData"
              :options="skillChartOptions"
              aria-label="Job demand by skill chart"
            />
            <div v-else class="empty-state">
              <i class="ti ti-chart-bar-off"></i>
              <div class="fw-semibold">No skill demand data yet</div>
              <small class="text-muted">Required skills will appear once drives include them.</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import BaseChart from "@/components/shared/BaseChart.vue";
import api from "@/services/api";

const searchQuery = ref("");
const loading = ref(false);
const error = ref("");
const dashboard = ref({
  stats: {},
  analytics: {
    monthly: [],
    skill_demand: [],
    application_funnel: {},
  },
});

const analytics = computed(() => dashboard.value.analytics || {});
const stats = computed(() => dashboard.value.stats || {});
const monthly = computed(() => analytics.value.monthly || []);
const skillDemand = computed(() => analytics.value.skill_demand || []);
const funnel = computed(() => analytics.value.application_funnel || {});

const cards = computed(() => [
  {
    title: "Applications",
    value: stats.value.applications || 0,
    note: "Application funnel",
  },
  {
    title: "Placements",
    value: funnel.value.selected || 0,
    note: "Selected outcomes",
  },
  {
    title: "Approvals",
    value: Number(stats.value.pending_companies || 0) + Number(stats.value.pending_drives || 0),
    note: "Companies and drives pending",
  },
]);

const filteredCards = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return cards.value;
  return cards.value.filter((item) =>
    [item.title, item.note].some((field) =>
      String(field || "")
        .toLowerCase()
        .includes(query),
    ),
  );
});

const monthlyChartData = computed(() => ({
  labels: monthly.value.map((item) => item.label),
  datasets: [
    {
      label: "Applications",
      data: monthly.value.map((item) => item.applications),
      borderColor: "#2563eb",
      backgroundColor: "rgba(37, 99, 235, 0.12)",
      tension: 0.35,
      fill: true,
    },
    {
      label: "Placements",
      data: monthly.value.map((item) => item.placements),
      borderColor: "#10b981",
      backgroundColor: "rgba(16, 185, 129, 0.12)",
      tension: 0.35,
      fill: true,
    },
  ],
}));

const funnelChartData = computed(() => ({
  labels: ["Applied", "Shortlisted", "Selected", "Rejected"],
  datasets: [
    {
      data: [
        funnel.value.applied || 0,
        funnel.value.shortlisted || 0,
        funnel.value.selected || 0,
        funnel.value.rejected || 0,
      ],
      backgroundColor: ["#2563eb", "#f59e0b", "#10b981", "#ef4444"],
      borderColor: "#ffffff",
      borderWidth: 4,
      hoverOffset: 6,
    },
  ],
}));

const skillChartData = computed(() => ({
  labels: skillDemand.value.map((item) => item.skill),
  datasets: [
    {
      label: "Drives",
      data: skillDemand.value.map((item) => item.count),
      backgroundColor: "#2563eb",
      borderRadius: 8,
      maxBarThickness: 44,
    },
  ],
}));

const lineChartOptions = {
  plugins: {
    legend: {
      position: "bottom",
      labels: { usePointStyle: true, boxWidth: 8 },
    },
  },
  scales: {
    y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: "#eef2f7" } },
    x: { grid: { display: false } },
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

const skillChartOptions = {
  indexAxis: "y",
  plugins: {
    legend: { display: false },
  },
  scales: {
    x: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: "#eef2f7" } },
    y: { grid: { display: false } },
  },
};

const loadAnalytics = async () => {
  loading.value = true;
  error.value = "";
  try {
    const response = await api.get("/admin/dashboard");
    dashboard.value = response.data;
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load analytics.";
  } finally {
    loading.value = false;
  }
};

onMounted(loadAnalytics);
</script>

<style scoped>
.mini-panel,
.analytics-panel {
  background: #fff;
  border: 1px solid #e9eef5;
  border-radius: 1rem;
}

.mini-panel {
  padding: 1.2rem;
  height: 100%;
}

.pill-label {
  align-self: flex-start;
  border-radius: 999px;
  background: #eef4ff;
  color: #2563eb;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.35rem 0.75rem;
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
  color: #64748b;
}

.empty-state i {
  font-size: 2rem;
}
</style>
