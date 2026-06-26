<template>
  <header class="topbar">
    <div class="topbar-left">
      <div class="search-box">
        <i class="ti ti-search"></i>
        <input
          :value="searchQuery"
          @input="$emit('update:searchQuery', $event.target.value)"
          type="text"
          class="form-control border-0"
          placeholder="Search drives, companies, skills..."
        />
      </div>
    </div>

    <div class="topbar-right">
      <button class="icon-btn" type="button" title="Theme">
        <i class="ti ti-moon-stars"></i>
      </button>
      <button class="icon-btn" type="button" title="Notifications">
        <i class="ti ti-bell"></i>
      </button>

      <div class="user-profile">
        <div class="avatar">{{ initials }}</div>
        <div class="user-info">
          <div class="user-name">{{ studentName }}</div>
          <small>Student</small>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useStudentStore } from "@/stores/studentStore";

defineProps({
  searchQuery: {
    type: String,
    default: "",
  },
});

defineEmits(["update:searchQuery"]);

const studentStore = useStudentStore();
const { profile } = storeToRefs(studentStore);

const studentName = computed(() => profile.value?.name || "Student");

const initials = computed(() => {
  return (
    studentName.value
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("") || "ST"
  );
});
</script>

<style scoped>
.topbar {
  height: 72px;
  background: white;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  gap: 1rem;
}

.topbar-left {
  flex: 1;
}

.search-box {
  width: min(420px, 100%);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 0.5rem 1rem;
}

.search-box i {
  color: #6c757d;
}

.search-box input {
  background: transparent;
  box-shadow: none;
}

.search-box input:focus {
  box-shadow: none;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.icon-btn {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  background: #fff;
  color: #495057;
  display: grid;
  place-items: center;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: #f8f9fa;
  transform: translateY(-1px);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-left: 0.8rem;
  border-left: 1px solid #e9ecef;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0d6efd, #3b82f6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  line-height: 1;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-info small {
  color: #6c757d;
}

@media (max-width: 768px) {
  .search-box {
    width: 220px;
  }

  .user-info {
    display: none;
  }
}
</style>
