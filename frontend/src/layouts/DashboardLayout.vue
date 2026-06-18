<template>
  <div class="dashboard-layout">
    <AppSidebar />

    <div class="dashboard-main">
      <AppTopbar />

      <main class="dashboard-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import AppSidebar from "@/components/dashboard/AppSidebar.vue";
import AppTopbar from "@/components/dashboard/AppTopbar.vue";
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

.dashboard-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f6f8fb;
}

.dashboard-content {
  flex: 1;
  padding: 1.5rem;
}
</style>
