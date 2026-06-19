<template>
  <DashboardLayout>
    <PageHeader title="Dashboard" subtitle="Everything you need at a glance.">
      <template #actions>
        <button type="button" class="btn btn-primary">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="icon icon-tabler icons-tabler-outline icon-tabler-download"
          >
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
            <path d="M7 11l5 5l5 -5" />
            <path d="M12 4l0 12" /></svg
          >Export
        </button>
      </template>
    </PageHeader>

    <div class="row g-4 mb-4">
      <div class="col-md-3">
        <StatCard title="Students" :value="1248" />
      </div>

      <div class="col-md-3">
        <StatCard title="Companies" :value="142" />
      </div>

      <div class="col-md-3">
        <StatCard title="Drives" :value="24" />
      </div>

      <div class="col-md-3">
        <StatCard title="Applications" :value="7856" />
      </div>
    </div>
    <div class="row mt-4">
      <div class="col-lg-8">
        <!-- Main Widget -->
        <ActionList title="Pending Approvals" :items="pending" />
      </div>

      <div class="col-lg-4">
        <RecentActivity title="Recent Activity" :activities="activities" />
      </div>
    </div>
    <div class="row mt-4">
      <div class="col-12">
        <DataTable :headers="headers" :rows="drives" />
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import StatCard from "@/components/shared/StatCard.vue";
import DataTable from "@/components/shared/DataTable.vue";
import RecentActivity from "@/components/shared/RecentActivity.vue";
import ActionList from "@/components/shared/ActionsList.vue";
import PageHeader from "@/components/shared/PageHeader.vue";

const activities = [
  {
    message: "Google India approved",
    time: "10 mins ago",
    color: "success",
  },
  {
    message: "Amazon drive created",
    time: "1 hour ago",
    color: "primary",
  },
];

const pending = [
  {
    title: "Google India",
    subtitle: "Company",
  },
  {
    title: "Amazon Backend Intern",
    subtitle: "Drive",
  },
];

const headers = [
  {
    key: "company",
    label: "Company",
  },
  {
    key: "role",
    label: "Role",
  },
  {
    key: "deadline",
    label: "Deadline",
  },
  {
    key: "applicants",
    label: "Applicants",
  },
  {
    key: "status",
    label: "Status",
  },
];

const drives = [
  {
    company: "Google",
    role: "SDE Intern",
    deadline: "20 Jun",
    applicants: 120,
    status: "Open",
  },
  {
    company: "Amazon",
    role: "Backend Intern",
    deadline: "25 Jun",
    applicants: 85,
    status: "Pending",
  },
];
</script>
