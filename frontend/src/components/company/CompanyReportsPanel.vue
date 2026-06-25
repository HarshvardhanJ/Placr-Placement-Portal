<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <div class="d-flex align-items-start justify-content-between gap-3 mb-4">
        <div>
          <h6 class="mb-1 fw-semibold">Reports</h6>
          <small class="text-muted">Download-ready summary cards for your placement team.</small>
        </div>
        <button
          class="btn btn-primary btn-sm"
          disabled
          title="CSV export is part of the backend jobs milestone and is not enabled yet"
        >
          <i class="ti ti-download me-2"></i>Export CSV
        </button>
      </div>

      <div class="row g-3 mb-4">
        <div v-for="card in reportCards" :key="card.label" class="col-12 col-md-4">
          <div class="report-tile border rounded-4 p-3 h-100">
            <div class="fw-semibold">{{ card.label }}</div>
            <div class="display-6 fw-bold my-2">{{ card.value }}</div>
            <small class="text-muted">{{ card.caption }}</small>
          </div>
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2">
        <RouterLink to="/company/placements" class="btn btn-outline-primary btn-sm">
          View Placements
        </RouterLink>
        <RouterLink to="/company/applications" class="btn btn-outline-secondary btn-sm">
          Review Applications
        </RouterLink>
        <RouterLink to="/company/interviews" class="btn btn-outline-secondary btn-sm">
          Interview Schedule
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useCompanyStore } from "@/stores/companyStore";

const store = useCompanyStore();
const { placements, dashboard } = storeToRefs(store);

const reportCards = computed(() => {
  const totalPlacements = placements.value?.length || 0;
  const offersMade = dashboard.value?.stats?.offers_made || 0;
  const totalApplications = dashboard.value?.stats?.total_applications || 0;

  return [
    {
      label: "Applications",
      value: totalApplications,
      caption: "Across all company drives",
    },
    {
      label: "Offers",
      value: offersMade,
      caption: "Candidates selected so far",
    },
    {
      label: "Placements",
      value: totalPlacements,
      caption: "Confirmed placement records",
    },
  ];
});
</script>

<style scoped>
.report-tile {
  background: #fff;
}
</style>
