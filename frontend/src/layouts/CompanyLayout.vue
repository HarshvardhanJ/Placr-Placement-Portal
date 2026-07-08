<template>
  <div class="company-layout">
    <CompanySidebar />

    <div class="company-main">
      <CompanyTopbar
        :search-query="searchQuery"
        :show-search="showSearch"
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
import CompanySidebar from "@/components/company/CompanySidebar.vue";
import CompanyTopbar from "@/components/company/CompanyTopbar.vue";

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
}

.company-page {
  max-width: 100%;
}
</style>
