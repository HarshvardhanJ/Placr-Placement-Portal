<template>
  <div class="student-layout">
    <div
      v-if="sidebarOpen"
      class="student-sidebar-backdrop"
      @click="sidebarOpen = false"
    ></div>
    <StudentSidebar
      :class="{ 'is-open': sidebarOpen }"
      @navigate="sidebarOpen = false"
    />
    <div class="student-main">
      <StudentTopbar
        :search-query="searchQuery"
        :show-search="showSearch"
        @toggle-sidebar="sidebarOpen = true"
        @update:search-query="$emit('update:searchQuery', $event)"
      />
      <main class="student-content">
        <div class="student-page">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import StudentSidebar from "@/components/student/StudentSidebar.vue";
import StudentTopbar from "@/components/student/StudentTopbar.vue";

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
.student-layout {
  display: flex;
  min-height: 100vh;
  background: #f6f8fb;
}

.student-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.student-content {
  flex: 1;
  padding: 1.5rem;
  min-width: 0;
}

.student-page {
  max-width: 100%;
}

@media (max-width: 991.98px) {
  .student-content {
    padding: 1rem;
  }

  .student-sidebar-backdrop {
    position: fixed;
    inset: 0;
    z-index: 1030;
    background: rgba(15, 23, 42, 0.38);
  }
}

@media (max-width: 575.98px) {
  .student-content {
    padding: 0.75rem;
  }
}
</style>
