<template>
  <header class="topbar">
    <button
      type="button"
      class="btn btn-outline-secondary menu-btn"
      aria-label="Open navigation"
      @click="$emit('toggleSidebar')"
    >
      <i class="ti ti-menu-2"></i>
    </button>

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

defineEmits(["update:searchQuery", "toggleSidebar"]);
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

.menu-btn {
  display: none;
  width: 42px;
  height: 42px;
  padding: 0;
  place-items: center;
  flex-shrink: 0;
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
  .topbar {
    height: auto;
    min-height: 64px;
    padding: 0.75rem;
  }

  .menu-btn {
    display: grid;
  }

  .search-box {
    width: 100%;
  }

  .user-info {
    display: none;
  }
}

@media (max-width: 575.98px) {
  .topbar {
    flex-wrap: wrap;
  }

  .topbar-left {
    flex: 1 0 calc(100% - 56px);
    order: 3;
  }
}
</style>
