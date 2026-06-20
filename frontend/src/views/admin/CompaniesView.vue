<template>
  <DashboardLayout>
    <PageHeader
      title="Companies"
      subtitle="Manage company accounts, approvals, and status."
    >
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

    <div class="card shadow-sm border-0 mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-center">
          <div class="col-lg-7">
            <div class="search-wrap">
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
                class="search-icon"
              >
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>

              <input
                v-model="searchQuery"
                type="text"
                class="form-control border-0 shadow-none"
                placeholder="Search by company name or industry..."
              />
            </div>
          </div>

          <div class="col-lg-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">All Statuses</option>
              <option value="approved">Approved</option>
              <option value="pending">Pending</option>
              <option value="inactive">Inactive</option>
              <option value="blacklisted">Blacklisted</option>
            </select>
          </div>

          <div class="col-lg-2">
            <button
              class="btn btn-outline-secondary w-100"
              type="button"
              @click="clearFilters"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <DataTable title="Companies" :headers="headers" :rows="filteredCompanies">
      <template #status="{ row }">
        <span class="badge rounded-pill" :class="statusBadgeClass(row.status)">
          {{ row.status }}
        </span>
      </template>

      <template #actions="{ row }">
        <div class="d-flex flex-wrap gap-2">
          <button
            class="btn btn-sm btn-outline-primary"
            @click="viewCompany(row)"
          >
            View
          </button>

          <button
            v-if="row.status === 'Pending'"
            class="btn btn-sm btn-outline-success"
            @click="approveCompany(row)"
          >
            Approve
          </button>

          <button
            v-if="row.status === 'Approved'"
            class="btn btn-sm btn-outline-warning"
            @click="confirmDeactivate(row)"
          >
            Deactivate
          </button>

          <button
            v-if="row.status === 'Inactive'"
            class="btn btn-sm btn-outline-success"
            @click="activateCompany(row)"
          >
            Activate
          </button>

          <button
            v-if="row.status === 'Blacklisted'"
            class="btn btn-sm btn-outline-success"
            @click="restoreCompany(row)"
          >
            Restore
          </button>

          <button
            v-if="row.status === 'Pending'"
            class="btn btn-sm btn-outline-danger"
            @click="confirmReject(row)"
          >
            Reject
          </button>

          <button
            v-if="row.status !== 'Blacklisted'"
            class="btn btn-sm btn-outline-danger"
            @click="confirmBlacklist(row)"
          >
            Blacklist
          </button>
        </div>
      </template>
    </DataTable>

    <CompanyDetailsModal
      :show="showCompanyModal"
      :company="selectedCompany"
      @close="showCompanyModal = false"
    />
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from "vue";

import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";
import CompanyDetailsModal from "@/components/admin/CompanyDetailsModal.vue";
import StatCard from "@/components/shared/StatCard.vue";

const searchQuery = ref("");
const statusFilter = ref("");

const selectedCompany = ref(null);
const showCompanyModal = ref(false);

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
    industry: "Semiconductors",
    status: "Blacklisted",
    drives: 4,
  },
  {
    id: 4,
    name: "Adobe",
    industry: "Software",
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

const stats = computed(() => [
  { title: "Total Companies", value: companies.value.length },
  {
    title: "Pending Approval",
    value: companies.value.filter((c) => c.status === "Pending").length,
  },
  {
    title: "Approved",
    value: companies.value.filter((c) => c.status === "Approved").length,
  },
  {
    title: "Blacklisted",
    value: companies.value.filter((c) => c.status === "Blacklisted").length,
  },
]);

const filteredCompanies = computed(() => {
  return companies.value.filter((company) => {
    const query = searchQuery.value.toLowerCase();

    const matchesSearch =
      company.name.toLowerCase().includes(query) ||
      company.industry.toLowerCase().includes(query);

    const matchesStatus =
      !statusFilter.value ||
      company.status.toLowerCase() === statusFilter.value;

    return matchesSearch && matchesStatus;
  });
});

const clearFilters = () => {
  searchQuery.value = "";
  statusFilter.value = "";
};

const statusBadgeClass = (status) => {
  switch (status) {
    case "Approved":
      return "text-bg-success";
    case "Pending":
      return "text-bg-warning";
    case "Inactive":
      return "text-bg-secondary";
    case "Blacklisted":
      return "text-bg-danger";
    default:
      return "text-bg-light";
  }
};

const viewCompany = (company) => {
  selectedCompany.value = company;
  showCompanyModal.value = true;
};

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
</script>

<style scoped>
.search-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f8fafc;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  padding: 0.6rem 0.9rem;
}

.search-icon {
  color: #6b7280;
  flex-shrink: 0;
}
</style>
