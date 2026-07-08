<template>
  <DashboardLayout v-model:search-query="searchQuery">
    <PageHeader title="Dashboard" subtitle="Everything you need at a glance.">
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink to="/admin/companies" class="btn btn-outline-primary">
            Companies
          </RouterLink>
          <RouterLink to="/admin/drives" class="btn btn-primary">
            <i class="ti ti-briefcase me-2"></i>View Drives
          </RouterLink>
        </div>
      </template>
    </PageHeader>

    <div class="admin-hero shadow-sm mb-4">
      <div>
        <div class="eyebrow mb-2">Placement cell overview</div>
        <h3 class="fw-bold mb-2">
          Approve faster, track activity, and keep your pipeline moving.
        </h3>
        <p class="text-secondary mb-0">
          A single workspace for students, companies, drives, and applications.
        </p>
      </div>

      <div class="hero-links">
        <RouterLink to="/admin/companies" class="hero-link">
          <i class="ti ti-building"></i>
          <span>Companies</span>
        </RouterLink>
        <RouterLink to="/admin/students" class="hero-link">
          <i class="ti ti-users"></i>
          <span>Students</span>
        </RouterLink>
        <RouterLink to="/admin/analytics" class="hero-link">
          <i class="ti ti-chart-bar"></i>
          <span>Analytics</span>
        </RouterLink>
        <RouterLink to="/admin/reports" class="hero-link">
          <i class="ti ti-report-analytics"></i>
          <span>Reports</span>
        </RouterLink>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div
        v-for="stat in stats"
        :key="stat.title"
        class="col-12 col-sm-6 col-xl-3"
      >
        <StatCard :title="stat.title" :value="stat.value" />
      </div>
    </div>

    <div class="row g-4 mb-4">
      <div class="col-xl-8">
        <ActionList
          title="Pending Approvals"
          :items="filteredPending"
        />
      </div>

      <div class="col-xl-4">
        <RecentActivity
          title="Recent Activity"
          :activities="filteredRecentActivity"
        />
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12">
        <DataTable
          title="Recent Drives"
          :headers="headers"
          :rows="filteredRecentDrives"
        >
          <template #approval_status="{ row }">
            <span
              class="badge rounded-pill"
              :class="{
                'text-bg-success': row.approval_status === 'approved',
                'text-bg-warning': row.approval_status === 'pending',
                'text-bg-danger': row.approval_status === 'rejected',
                'text-bg-secondary': row.approval_status === 'closed',
              }"
            >
              {{ row.approval_status }}
            </span>
          </template>
        </DataTable>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import StatCard from "@/components/shared/StatCard.vue";
import DataTable from "@/components/shared/DataTable.vue";
import RecentActivity from "@/components/shared/RecentActivity.vue";
import ActionList from "@/components/shared/ActionsList.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import api from "@/services/api";

const loading = ref(false);
const searchQuery = ref("");

const dashboard = ref({
  stats: {
    students: 0,
    companies: 0,
    drives: 0,
    applications: 0,
  },
  pending: [],
  recent_activity: [],
  recent_drives: [],
});

const headers = [
  { key: "company_name", label: "Company" },
  { key: "job_location", label: "Location" },
  { key: "job_title", label: "Role" },
  { key: "application_deadline", label: "Deadline" },
  { key: "applicants", label: "Applicants" },
  { key: "approval_status", label: "Status" },
];

const loadDashboard = async () => {
  try {
    loading.value = true;

    const response = await api.get("/admin/dashboard");

    dashboard.value = response.data;
  } catch (error) {
    console.error("Failed to load dashboard:", error);
  } finally {
    loading.value = false;
  }
};

const stats = computed(() => [
  {
    title: "Students",
    value: dashboard.value.stats.students,
  },
  {
    title: "Companies",
    value: dashboard.value.stats.companies,
  },
  {
    title: "Drives",
    value: dashboard.value.stats.drives,
  },
  {
    title: "Applications",
    value: dashboard.value.stats.applications,
  },
]);

const normalize = (value = "") => String(value || "").toLowerCase();

const matchesQuery = (fields) => {
  const query = normalize(searchQuery.value).trim();
  if (!query) return true;
  return fields.some((field) => normalize(field).includes(query));
};

const filteredPending = computed(() =>
  (dashboard.value.pending || []).filter((item) =>
    matchesQuery([item.title, item.subtitle, item.type]),
  ),
);

const filteredRecentActivity = computed(() =>
  (dashboard.value.recent_activity || []).filter((activity) =>
    matchesQuery([activity.message, activity.time]),
  ),
);

const filteredRecentDrives = computed(() =>
  (dashboard.value.recent_drives || []).filter((drive) =>
    matchesQuery([
      drive.company_name,
      drive.job_location,
      drive.job_title,
      drive.approval_status,
    ]),
  ),
);

onMounted(() => {
  loadDashboard();
});
</script>

<style scoped>
.admin-hero {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 1.5rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
  border: 1px solid #e9eef5;
  border-radius: 22px;
  padding: 1.35rem 1.5rem;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.35rem 0.75rem;
  background: #eef4ff;
  color: #2563eb;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.hero-links {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
  min-width: 260px;
}

.hero-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  justify-content: flex-start;
  padding: 0.8rem 1rem;
  border-radius: 14px;
  background: #fff;
  border: 1px solid #e9eef5;
  color: #1f2937;
  text-decoration: none;
  font-weight: 600;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease,
    border-color 0.15s ease;
}

.hero-link:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08);
  border-color: #cfe0ff;
}

@media (max-width: 991.98px) {
  .admin-hero {
    flex-direction: column;
  }

  .hero-links {
    min-width: 0;
  }
}

@media (max-width: 575.98px) {
  .hero-links {
    grid-template-columns: 1fr;
  }
}
</style>
