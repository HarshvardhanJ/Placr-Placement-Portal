<template>
  <DataTable title="Active Job Drives" :headers="headers" :rows="drives">
    <template #header-actions>
      <RouterLink
        to="/company/drives"
        class="btn btn-link btn-sm text-decoration-none"
      >
        View All
      </RouterLink>
    </template>

    <template #role="{ row }">
      <div class="d-flex align-items-center gap-3">
        <div class="drive-avatar">{{ initialLetter(row.job_title) }}</div>
        <div style="min-width: 0">
          <div class="fw-semibold text-truncate">{{ row.job_title }}</div>
          <small class="text-muted text-truncate d-block">{{
            row.company_name
          }}</small>
        </div>
      </div>
    </template>

    <template #applicants_count="{ row }">
      <span class="text-center d-block">{{ row.applicants_count }}</span>
    </template>

    <template #status="{ row }">
      <span class="badge rounded-pill" :class="statusBadgeClass(row.status)">
        {{ displayStatus(row.status) }}
      </span>
    </template>

    <template #row_actions="{ row }">
      <div class="d-flex flex-wrap justify-content-end gap-2">
        <RouterLink
          :to="`/company/drives/${row.drive_id}`"
          class="btn btn-sm btn-outline-dark"
        >
          Open
        </RouterLink>
        <RouterLink
          :to="`/company/applications?drive=${row.drive_id}`"
          class="btn btn-sm btn-outline-primary"
        >
          Applicants
        </RouterLink>
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import DataTable from "@/components/shared/DataTable.vue";

defineProps({
  drives: {
    type: Array,
    default: () => [],
  },
});

const headers = [
  { key: "role", label: "Company & Role" },
  { key: "applicants_count", label: "Applicants" },
  { key: "status", label: "Status" },
  { key: "row_actions", label: "" },
];

const initialLetter = (value = "") =>
  String(value).trim().charAt(0).toUpperCase() || "D";

const displayStatus = (status = "") => {
  const map = {
    shortlisting: "Shortlisting",
    interviewing: "Interviewing",
    active: "Active",
  };
  return map[status] || "Active";
};

const statusBadgeClass = (status = "") => {
  if (status === "shortlisting")
    return "bg-warning-subtle text-warning-emphasis";
  if (status === "interviewing") return "bg-primary-subtle text-primary";
  if (status === "active") return "bg-success-subtle text-success";
  return "bg-light text-muted border";
};
</script>

<style scoped>
.drive-avatar {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: linear-gradient(135deg, #eef2f7, #e0e7ff);
  color: #4b5563;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>
