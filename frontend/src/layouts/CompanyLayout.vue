<template>
  <div class="company-layout">
    <div
      v-if="sidebarOpen"
      class="company-sidebar-backdrop"
      @click="sidebarOpen = false"
    ></div>
    <CompanySidebar
      :class="{ 'is-open': sidebarOpen }"
      @navigate="sidebarOpen = false"
    />

    <div class="company-main">
      <CompanyTopbar
        :search-query="searchQuery"
        :show-search="showSearch"
        @toggle-sidebar="sidebarOpen = true"
        @update:search-query="$emit('update:searchQuery', $event)"
      />

      <main class="company-content">
        <div class="company-page">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import CompanySidebar from "@/components/company/CompanySidebar.vue";
import CompanyTopbar from "@/components/company/CompanyTopbar.vue";

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
</script>

<style scoped>
.company-layout {
  display: flex;
  min-height: 100vh;
  background: #f6f8fb;
}

.company-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.company-content {
  flex: 1;
  padding: 1.5rem;
  min-width: 0;
}

.company-page {
  max-width: 100%;
}

@media (max-width: 991.98px) {
  .company-content {
    padding: 1rem;
  }

  .company-sidebar-backdrop {
    position: fixed;
    inset: 0;
    z-index: 1030;
    background: rgba(15, 23, 42, 0.38);
  }
}

@media (max-width: 575.98px) {
  .company-content {
    padding: 0.75rem;
  }
}
</style>
