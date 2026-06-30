<template>
  <DashboardLayout>
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

    <div class="analytics-shell">
      <div class="analytics-banner">
        <div class="eyebrow mb-2">Coming soon</div>
        <h3 class="fw-bold mb-2">
          This space is ready for charts and trend analysis.
        </h3>
        <p class="text-secondary mb-0">
          You can plug in monthly placements, company approvals, application
          funnels, and drive health metrics here later without changing the
          route structure.
        </p>
      </div>

      <div class="row g-3 mt-1">
        <div class="col-12 col-lg-4" v-for="item in cards" :key="item.title">
          <div class="mini-panel shadow-sm">
            <div class="text-secondary small text-uppercase fw-semibold mb-1">
              {{ item.title }}
            </div>
            <div class="fw-bold fs-3">{{ item.value }}</div>
            <small class="text-secondary">{{ item.note }}</small>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";

const cards = [
  { title: "Applications", value: "—", note: "Application funnel" },
  { title: "Placements", value: "—", note: "Monthly outcomes" },
  { title: "Approvals", value: "—", note: "Company and drive status" },
];
</script>

<style scoped>
.analytics-shell {
  display: grid;
  gap: 1.25rem;
}

.analytics-banner {
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
  border: 1px solid #e9eef5;
  border-radius: 22px;
  padding: 1.5rem;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.75rem;
  background: #eef4ff;
  color: #2563eb;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.mini-panel {
  background: #fff;
  border: 1px solid #e9eef5;
  border-radius: 18px;
  padding: 1.2rem;
  height: 100%;
}
</style>
