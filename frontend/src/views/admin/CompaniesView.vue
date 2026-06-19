<template>
  <DashboardLayout>
    <PageHeader
      title="Companies"
      subtitle="Manage company accounts, approvals, and status."
    >
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
        </div>
      </div>
    </div>

    <DataTable title="Companies" :headers="headers" :rows="filteredCompanies">
      <template #actions="{ row }">
        <div class="btn-group btn-group-sm">
          <button class="btn btn-outline-primary" @click="viewCompany(row)">
            View
          </button>

          <button
            v-if="row.status === 'Pending'"
            class="btn btn-outline-success"
            @click="approveCompany(row)"
          >
            Approve
          </button>

          <button
            v-if="row.status === 'Approved'"
            class="btn btn-outline-warning"
            @click="confirmDeactivate(row)"
          >
            Deactivate
          </button>

          <button
            v-if="row.status === 'Inactive'"
            class="btn btn-outline-success"
            @click="activateCompany(row)"
          >
            Activate
          </button>

          <button
            v-if="row.status === 'Blacklisted'"
            class="btn btn-outline-success"
            @click="restoreCompany(row)"
          >
            Restore
          </button>

          <button
            class="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split"
            data-bs-toggle="dropdown"
          ></button>

          <ul class="dropdown-menu dropdown-menu-end">
            <li v-if="row.status === 'Pending'">
              <a
                class="dropdown-item text-danger"
                href="#"
                @click.prevent="confirmReject(row)"
              >
                Reject
              </a>
            </li>

            <li
              v-if="
                row.status === 'Approved' ||
                row.status === 'Pending' ||
                row.status === 'Inactive'
              "
            >
              <a
                class="dropdown-item text-danger"
                href="#"
                @click.prevent="confirmBlacklist(row)"
              >
                Blacklist
              </a>
            </li>
          </ul>
        </div>
      </template>
    </DataTable>
  </DashboardLayout>
  <CompanyDetailsModal
    :show="showCompanyModal"
    :company="selectedCompany"
    @close="showCompanyModal = false"
  />
</template>

<script setup>
import { ref, computed } from "vue";

import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";
import CompanyDetailsModal from "@/components/admin/CompanyDetailsModal.vue";
import StatCard from "@/components/shared/StatCard.vue";

const selectedCompany = ref(null);
const showCompanyModal = ref(false);
const searchQuery = ref("");
const statusFilter = ref("");

const viewCompany = (company) => {
  selectedCompany.value = company;
  showCompanyModal.value = true;
};

const companies = ref([
  {
    id: 1,
    name: "Google",
    industry: "Technology",
    status: "Approved",
    drives: 5,
  },
  {
    id: 2,
    name: "Amazon",
    industry: "Technology",
    status: "Pending",
    drives: 2,
  },
  {
    id: 3,
    name: "NVIDIA",
    industry: "Technology",
    status: "Blacklisted",
    drives: 4,
  },
  {
    id: 4,
    name: "Adobe",
    industry: "Technology",
    status: "Inactive",
    drives: 1,
  },
]);

const headers = [
  { key: "name", label: "Company" },
  { key: "industry", label: "Industry" },
  { key: "status", label: "Status" },
  { key: "drives", label: "Drives" },
  { key: "actions", label: "Actions" },
];

const approveCompany = (company) => {
  company.status = "Approved";
};

const rejectCompany = (company) => {
  companies.value = companies.value.filter((c) => c.id !== company.id);
};

const confirmReject = (company) => {
  if (window.confirm(`Reject ${company.name}?`)) {
    rejectCompany(company);
  }
};

const deactivateCompany = (company) => {
  company.status = "Inactive";
};

const confirmDeactivate = (company) => {
  if (window.confirm(`Deactivate ${company.name}?`)) {
    deactivateCompany(company);
  }
};

const activateCompany = (company) => {
  company.status = "Approved";
};

const blacklistCompany = (company) => {
  company.status = "Blacklisted";
};

const confirmBlacklist = (company) => {
  if (window.confirm(`Blacklist ${company.name}?`)) {
    blacklistCompany(company);
  }
};

const restoreCompany = (company) => {
  company.status = "Approved";
};

const totalCompanies = computed(() => companies.value.length);

const pendingCompanies = computed(
  () => companies.value.filter((c) => c.status === "Pending").length,
);

const filteredCompanies = computed(() => {
  return companies.value.filter((company) => {
    const matchesSearch =
      company.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      company.industry.toLowerCase().includes(searchQuery.value.toLowerCase());

    const matchesStatus =
      !statusFilter.value ||
      company.status.toLowerCase() === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});
</script>
