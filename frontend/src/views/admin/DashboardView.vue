<template>
  <DashboardLayout>
    <h2 class="mb-4">Dashboard Overview</h2>

    <div class="row g-4">
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
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from "@/layouts/DashboardLayout.vue";
import StatCard from "@/components/dashboard/StatCard.vue";
</script>
