<template>
  <StudentLayout v-model:search-query="searchQuery">
    <PageHeader :title="title" :subtitle="subtitle" />

    <div class="card shadow-sm border-0">
      <div class="card-body p-4">
        <StudentEmptyState :icon="icon" :title="title" :subtitle="body">
          <template #actions>
            <div class="d-flex flex-wrap gap-2">
              <RouterLink v-for="item in actions" :key="item.to" :to="item.to" class="btn btn-outline-primary btn-sm">
                {{ item.label }}
              </RouterLink>
            </div>
          </template>
        </StudentEmptyState>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { ref } from "vue";
import StudentLayout from "@/layouts/StudentLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StudentEmptyState from "./StudentEmptyState.vue";

defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
  body: {
    type: String,
    default: "This section is ready to be connected to the backend feature set.",
  },
  icon: {
    type: String,
    default: "ti-layout-dashboard-off",
  },
  actions: {
    type: Array,
    default: () => [],
  },
});

const searchQuery = ref("");
</script>
