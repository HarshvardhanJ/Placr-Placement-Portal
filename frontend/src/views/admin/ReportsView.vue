<template>
  <DashboardLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Reports"
      subtitle="Placement summaries and system-level reporting."
    >
      <template #actions>
        <RouterLink to="/admin/analytics" class="btn btn-outline-primary">
          <i class="ti ti-chart-bar me-2"></i>Analytics
        </RouterLink>
      </template>
    </PageHeader>

    <div class="reports-shell">
      <div class="reports-banner">
        <div class="eyebrow mb-2">Report center</div>
        <h3 class="fw-bold mb-2">
          Monthly reporting is handled by the backend job schedule.
        </h3>
        <p class="text-secondary mb-0">
          Student and company CSV exports are available from their own
          dashboards, where access control matches each user role.
        </p>
      </div>

      <div class="row g-3 mt-1">
        <div
          class="col-12 col-md-4"
          v-for="item in filteredItems"
          :key="item.title"
        >
          <div class="report-card shadow-sm">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <div class="fw-semibold">{{ item.title }}</div>
              <i :class="item.icon" class="ti fs-4 text-primary"></i>
            </div>
            <div class="text-secondary small">{{ item.note }}</div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import { computed, ref } from "vue";

const searchQuery = ref("");

const items = [
  {
    title: "Monthly Placement Report",
    note: "Company-wise and branch-wise summary",
    icon: "ti-file-report",
  },
  {
    title: "Drive Summary",
    note: "Approved, pending, and closed drives",
    icon: "ti-briefcase",
  },
  {
    title: "Applications Summary",
    note: "Status-wise application batches",
    icon: "ti-file-text",
  },
];

const filteredItems = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return items;
  return items.filter((item) =>
    [item.title, item.note].some((field) =>
      String(field || "")
        .toLowerCase()
        .includes(query),
    ),
  );
});
</script>

<style scoped>
.reports-shell {
  display: grid;
  gap: 1.25rem;
}

.reports-banner {
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

.report-card {
  background: #fff;
  border: 1px solid #e9eef5;
  border-radius: 18px;
  padding: 1.25rem;
  height: 100%;
}
</style>
