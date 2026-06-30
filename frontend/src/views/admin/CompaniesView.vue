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

    <div class="admin-hero shadow-sm mb-4">
      <div>
        <div class="eyebrow mb-2">Company registry</div>
        <h3 class="fw-bold mb-2">
          Review approvals, spot active companies, and keep the record clean.
        </h3>
        <p class="text-secondary mb-0">
          Manage company status, inspect their profile details, and quickly
          check how many drives each one has created.
        </p>
      </div>

      <div class="hero-metrics">
        <div class="mini-metric">
          <span>Companies</span>
          <strong>{{ stats[0].value }}</strong>
        </div>
        <div class="mini-metric">
          <span>Pending</span>
          <strong>{{ stats[1].value }}</strong>
        </div>
        <div class="mini-metric">
          <span>Approved</span>
          <strong>{{ stats[2].value }}</strong>
        </div>
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
        <div class="d-flex flex-wrap gap-2 justify-content-end">
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
import { ref, computed, onMounted, watch } from "vue";

import DashboardLayout from "@/layouts/DashboardLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import DataTable from "@/components/shared/DataTable.vue";
import CompanyDetailsModal from "@/components/admin/CompanyDetailsModal.vue";
import StatCard from "@/components/shared/StatCard.vue";
import api from "@/services/api";

const searchQuery = ref("");
const statusFilter = ref("");

const selectedCompany = ref(null);
const showCompanyModal = ref(false);
const loading = ref(false);

const companies = ref([]);

watch(searchQuery, async (value) => {
  try {
    const response = await api.get("/admin/companies", {
      params: {
        search: value,
      },
    });

    companies.value = response.data.map((company) => ({
      ...company,
      status: getCompanyStatus(company),
    }));
  } catch (err) {
    console.error(err);
  }
});

const loadCompanies = async () => {
  try {
    loading.value = true;

    const response = await api.get("/admin/companies");

    companies.value = response.data.map((company) => ({
      ...company,
      status: getCompanyStatus(company),
    }));
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const getCompanyStatus = (company) => {
  if (!company.is_active) return "Blacklisted";

  if (company.approval_status === "approved") return "Approved";

  return "Pending";
};

const headers = [
  { key: "name", label: "Company" },
  { key: "industry", label: "Industry" },
  { key: "status", label: "Status" },
  { key: "drives", label: "Drives" },
  { key: "actions", label: "Actions" },
];

const stats = computed(() => [
  {
    title: "Companies",
    value: companies.value.length,
  },
  {
    title: "Pending",
    value: companies.value.filter((c) => c.status === "Pending").length,
  },
  {
    title: "Approved",
    value: companies.value.filter((c) => c.status === "Approved").length,
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

const approveCompany = async (company) => {
  try {
    await api.put(`/admin/companies/${company.company_id}/approve`);
    company.status = "Approved";
  } catch (err) {
    console.error(err);
  }
};

const rejectCompany = async (company) => {
  try {
    await api.put(`/admin/companies/${company.company_id}/reject`);
    companies.value = companies.value.filter(
      (c) => c.company_id !== company.company_id,
    );
  } catch (err) {
    console.error(err);
  }
};

const confirmReject = (company) => {
  if (window.confirm(`Reject ${company.name}?`)) {
    rejectCompany(company);
  }
};

const activateCompany = (company) => {
  company.status = "Approved";
};

const blacklistCompany = async (company) => {
  try {
    await api.put(`/admin/companies/${company.company_id}/blacklist`);
    company.status = "Blacklisted";
  } catch (err) {
    console.error(err);
  }
};

const confirmBlacklist = (company) => {
  if (window.confirm(`Blacklist ${company.name}? YOU CAN'T UNDO THIS`)) {
    blacklistCompany(company);
  }
};

onMounted(() => {
  loadCompanies();
});
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

.hero-metrics {
  display: grid;
  gap: 0.75rem;
  min-width: 220px;
}

.mini-metric {
  background: #fff;
  border: 1px solid #e9eef5;
  border-radius: 16px;
  padding: 0.85rem 1rem;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
}

.mini-metric span {
  display: block;
  color: #64748b;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 800;
  margin-bottom: 0.2rem;
}

.mini-metric strong {
  font-size: 1.4rem;
  color: #111827;
}

@media (max-width: 991.98px) {
  .admin-hero {
    flex-direction: column;
  }

  .hero-metrics {
    min-width: 0;
  }
}
</style>
