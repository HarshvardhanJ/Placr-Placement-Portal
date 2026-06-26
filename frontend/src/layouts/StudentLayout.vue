<template>
  <div class="student-layout">
    <StudentSidebar />
    <div class="student-main">
      <StudentTopbar
        :search-query="searchQuery"
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
import StudentSidebar from "@/components/student/StudentSidebar.vue";
import StudentTopbar from "@/components/student/StudentTopbar.vue";

defineProps({
  searchQuery: {
    type: String,
    default: "",
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
}

.student-page {
  max-width: 100%;
}

@media (max-width: 991.98px) {
  .student-layout {
    flex-direction: column;
  }

  .student-content {
    padding: 1rem;
  }
}
</style>
