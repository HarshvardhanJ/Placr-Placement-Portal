<template>
  <DashboardLayout>
    <PageHeader title="Dashboard" subtitle="Everything you need at a glance.">
      <template #actions>
        <button
          type="button"
          class="btn btn-primary d-inline-flex align-items-center gap-2"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
            <path d="M7 11l5 5l5 -5" />
            <path d="M12 4l0 12" />
          </svg>
          <span>Export</span>
        </button>
      </template>
    </PageHeader>

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
          :items="dashboard.pending || []"
        />
      </div>

      <div class="col-xl-4">
        <RecentActivity
          title="Recent Activity"
          :activities="dashboard.recent_activity || []"
        />
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12">
        <DataTable
          title="Recent Drives"
          :headers="headers"
          :rows="dashboard.recent_drives"
        >
          <template #approval_status="{ row }">
            <span
              class="badge"
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

onMounted(() => {
  loadDashboard();
});
</script>
