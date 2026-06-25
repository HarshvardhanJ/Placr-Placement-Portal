<template>
  <CompanyLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Dashboard"
      subtitle="Track your placement drives, applicants, interviews, and offers."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink to="/company/drives?new=1" class="btn btn-primary">
            <i class="ti ti-plus me-2"></i>New Drive
          </RouterLink>
          <RouterLink to="/company/placements" class="btn btn-outline-primary">
            <i class="ti ti-trophy me-2"></i>Placements
          </RouterLink>
        </div>
      </template>
    </PageHeader>

    <div v-if="store.pendingApproval" class="pending-card text-center">
      <i class="ti ti-clock-hour-4 display-5 text-primary"></i>
      <h4 class="fw-bold mt-3 mb-1">Approval pending</h4>
      <p class="text-muted mb-0">
        Your company registration is awaiting admin approval. You'll get access
        to the dashboard as soon as it's approved.
      </p>
    </div>

    <template v-else>
      <div v-if="store.error" class="alert alert-danger">{{ store.error }}</div>

      <div class="tab-pills mb-4">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          type="button"
          class="tab-pill"
          :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key"
        >
          {{ tab.label }}
        </button>
      </div>

      <template v-if="activeTab === 'overview'">
        <div class="row g-3 mb-4">
          <div
            v-for="card in store.statsCards"
            :key="card.key"
            class="col-12 col-sm-6 col-xl-3"
          >
            <StatCard
              :title="card.label"
              :value="card.value"
              :icon="card.icon"
              :delta="card.delta"
            />
          </div>
        </div>

        <div class="row g-3">
          <div class="col-12 col-xl-8">
            <CompanyJobsTable :drives="filteredDrives" />
          </div>
          <div class="col-12 col-xl-4">
            <RecentApplicantsPanel :applicants="filteredApplicants" />
          </div>
        </div>
      </template>

      <template v-else-if="activeTab === 'analytics'">
        <CompanyAnalyticsPanel />
      </template>

      <template v-else-if="activeTab === 'placements'">
        <div class="row g-3 mb-4">
          <div
            v-for="card in store.placementStats"
            :key="card.key"
            class="col-12 col-sm-6 col-xl-3"
          >
            <StatCard
              :title="card.label"
              :value="card.value"
              :icon="card.icon"
            />
          </div>
        </div>

        <DataTable
          title="Recent Placements"
          :headers="placementHeaders"
          :rows="filteredPlacements"
        >
          <template #student_name="{ row }">
            <div class="fw-semibold">{{ row.student_name }}</div>
            <small class="text-muted">{{ row.roll_no }}</small>
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
                row.offer_letter_uploaded
                  ? 'text-bg-success'
                  : 'text-bg-secondary'
              "
            >
              {{ row.offer_letter_uploaded ? "Uploaded" : "Pending" }}
            </span>
          </template>

          <template #actions="{ row }">
            <RouterLink
              :to="`/company/drives/${row.drive_id}`"
              class="btn btn-sm btn-outline-primary"
            >
              Open Drive
            </RouterLink>
          </template>
        </DataTable>
      </template>

      <template v-else>
        <CompanyReportsPanel />
      </template>
    </template>
  </CompanyLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useCompanyStore } from "@/stores/companyStore";

import CompanyLayout from "@/layouts/CompanyLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StatCard from "@/components/shared/StatCard.vue";
import DataTable from "@/components/shared/DataTable.vue";
import CompanyJobsTable from "@/components/company/CompanyJobsTable.vue";
import RecentApplicantsPanel from "@/components/company/RecentApplicantsPanel.vue";
import CompanyAnalyticsPanel from "@/components/company/CompanyAnalyticsPanel.vue";
import CompanyReportsPanel from "@/components/company/CompanyReportsPanel.vue";

const store = useCompanyStore();

const activeTab = ref("overview");
const searchQuery = ref("");

const tabs = [
  { key: "overview", label: "Overview" },
  { key: "analytics", label: "Analytics" },
  { key: "placements", label: "Placements" },
  { key: "reports", label: "Reports" },
];

const placementHeaders = [
  { key: "student_name", label: "Student" },
  { key: "job_title", label: "Role" },
  { key: "salary", label: "Salary" },
  { key: "joining_date", label: "Joining" },
  { key: "offer_letter_uploaded", label: "Offer Letter" },
  { key: "actions", label: "Actions" },
];

const filteredDrives = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return store.activeDrives;
  return store.activeDrives.filter(
    (drive) =>
      drive.job_title?.toLowerCase().includes(query) ||
      drive.status?.toLowerCase().includes(query),
  );
});

const filteredApplicants = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return store.recentApplicants;
  return store.recentApplicants.filter(
    (applicant) =>
      applicant.student_name?.toLowerCase().includes(query) ||
      applicant.job_title?.toLowerCase().includes(query),
  );
});

const filteredPlacements = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return store.placements.slice(0, 8);
  return store.placements.filter(
    (placement) =>
      placement.student_name?.toLowerCase().includes(query) ||
      placement.roll_no?.toLowerCase().includes(query) ||
      placement.job_title?.toLowerCase().includes(query),
  );
});

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
  return d.toLocaleDateString([], { dateStyle: "medium" });
};

onMounted(async () => {
  await store.fetchDashboard();
  if (!store.pendingApproval) {
    await store.fetchPlacements().catch(() => null);
  }
});
</script>

<style scoped>
.tab-pills {
  display: inline-flex;
  gap: 0.35rem;
  background: #eef1f6;
  padding: 0.3rem;
  border-radius: 12px;
  flex-wrap: wrap;
}

.tab-pill {
  border: 0;
  background: transparent;
  padding: 0.45rem 1.1rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  color: #5f6b7a;
  transition: all 0.15s ease;
}

.tab-pill.active {
  background: #ffffff;
  color: #0d6efd;
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.08);
}

.pending-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  padding: 3rem 2rem;
  max-width: 520px;
  margin: 2rem auto;
}
</style>
