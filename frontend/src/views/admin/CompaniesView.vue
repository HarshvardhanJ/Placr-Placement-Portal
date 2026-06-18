<template>
  <DashboardLayout>
    <PageHeader
      title="Companies"
      subtitle="Manage company accounts, approvals, and status."
    />

    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-lg-6">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control"
              placeholder="Search by company name or industry..."
            />
          </div>

          <div class="col-lg-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">All Statuses</option>
              <option value="approved">Approved</option>
              <option value="pending">Pending</option>
              <option value="blacklisted">Blacklisted</option>
            </select>
          </div>

          <div class="col-lg-3">
            <button class="btn btn-outline-primary w-100">Search</button>
          </div>
        </div>
      </div>
    </div>

    <DataTable :headers="headers" :rows="companies" />
  </DashboardLayout>
</template>

<script setup>
import { ref } from "vue";

import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";

const searchQuery = ref("");
const statusFilter = ref("");

const headers = [
  { key: "name", label: "Company" },
  { key: "industry", label: "Industry" },
  { key: "status", label: "Status" },
];

const companies = [
  {
    name: "Google",
    industry: "Technology",
    status: "Approved",
    actions: "View",
  },
  {
    name: "Amazon",
    industry: "Technology",
    status: "Pending",
    actions: "Approve",
  },
  {
    name: "NVIDIA",
    industry: "Technology",
    status: "Approved",
    actions: "View",
  },
];
</script>
