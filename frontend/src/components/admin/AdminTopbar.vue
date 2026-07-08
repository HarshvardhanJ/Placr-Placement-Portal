<template>
  <header class="topbar">
    <div v-if="showSearch" class="topbar-left">
      <div class="search-box">
        <i class="ti ti-search"></i>

        <input
          :value="searchQuery"
          @input="$emit('update:searchQuery', $event.target.value)"
          type="text"
          class="form-control border-0"
          placeholder="Search students, companies, drives..."
        />
      </div>
    </div>
    <div v-else class="topbar-left"></div>

    <div class="topbar-right">
      <div class="user-profile">
        <div class="avatar">AD</div>

        <div class="user-info">
          <div class="user-name">Admin User</div>

          <small>Placement Cell</small>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
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

.icon-btn {
  width: 42px;
  height: 42px;

  border: 1px solid #e9ecef;
  border-radius: 12px;

  background: white;

  display: flex;
  align-items: center;
  justify-content: center;

  position: relative;

  color: #495057;

  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: #f8f9fa;
  border-color: #d0d7de;
}

.icon-btn svg {
  width: 20px;
  height: 20px;
}

.notification-dot {
  width: 8px;
  height: 8px;

  background: #dc3545;
  border-radius: 50%;

  position: absolute;
  top: 10px;
  right: 10px;

  border: 2px solid white;
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
