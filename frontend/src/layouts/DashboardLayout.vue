<template>
  <div class="dashboard-layout">
    <AdminSidebar />

    <div class="dashboard-main">
      <AdminTopbar />

      <main class="dashboard-content">
        <div class="dashboard-page">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import AdminSidebar from "@/components/admin/AdminSidebar.vue";
import AdminTopbar from "@/components/admin/AdminTopbar.vue";
import { onMounted } from "vue";
import { useAdminStore } from "@/stores/adminStore";

const adminStore = useAdminStore();

onMounted(() => {
  adminStore.fetchDashboardStats();
});
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background: #f6f8fb;
}

.dashboard-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.dashboard-content {
  flex: 1;
  padding: 1.5rem;
}

.dashboard-page {
  max-width: 100%;
}
</style>
