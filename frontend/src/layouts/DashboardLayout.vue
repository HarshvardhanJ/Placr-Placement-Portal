<template>
  <div class="dashboard-layout">
    <div
      v-if="sidebarOpen"
      class="dashboard-sidebar-backdrop"
      @click="sidebarOpen = false"
    ></div>

    <AdminSidebar
      :class="{ 'is-open': sidebarOpen }"
      @navigate="sidebarOpen = false"
    />

    <div class="dashboard-main">
      <AdminTopbar
        :search-query="searchQuery"
        :show-search="showSearch"
        @toggle-sidebar="sidebarOpen = true"
        @update:search-query="$emit('update:searchQuery', $event)"
      />

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
import { onMounted, ref } from "vue";
import { useAdminStore } from "@/stores/adminStore";

const adminStore = useAdminStore();
const sidebarOpen = ref(false);

defineProps({
  searchQuery: {
    type: String,
    default: "",
  },
  showSearch: {
    type: Boolean,
    default: true,
  },
});

defineEmits(["update:searchQuery"]);

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
  min-width: 0;
}

.dashboard-page {
  max-width: 100%;
}

.dashboard-sidebar-backdrop {
  display: none;
}

@media (max-width: 991.98px) {
  .dashboard-content {
    padding: 1rem;
  }

  .dashboard-sidebar-backdrop {
    position: fixed;
    inset: 0;
    z-index: 1030;
    display: block;
    background: rgba(15, 23, 42, 0.38);
  }
}

@media (max-width: 575.98px) {
  .dashboard-content {
    padding: 0.75rem;
  }
}
</style>
