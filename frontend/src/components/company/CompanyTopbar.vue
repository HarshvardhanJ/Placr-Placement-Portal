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
          placeholder="Search drives, applicants..."
        />
      </div>
    </div>

    <div class="topbar-right">
      <div class="user-profile">
        <div class="avatar">{{ initials }}</div>
        <div class="user-info">
          <div class="user-name">{{ companyName }}</div>
          <small>Company</small>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useCompanyStore } from "@/stores/companyStore";

defineProps({
  searchQuery: {
    type: String,
    default: "",
  },
});

defineEmits(["update:searchQuery"]);

const companyStore = useCompanyStore();
const { company } = storeToRefs(companyStore);

const companyName = computed(() => company.value?.name || "Company");

const initials = computed(() =>
  companyName.value
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("") || "CO",
);
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
}

.topbar-left {
  flex: 1;
}

.search-box {
  width: 360px;
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
  gap: 1rem;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-left: 1rem;
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
