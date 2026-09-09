<template>
  <header class="topbar">
    <div v-if="showSearch" class="d-flex align-items-center gap-3">
      <input
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
        type="text"
        class="form-control"
        placeholder="Search..."
      />
    </div>
    <div v-else></div>

    <div>
      <span class="fw-semibold"> Admin User </span>
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
  height: 70px;
  background: white;
  border-bottom: 1px solid #dee2e6;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 0 1.5rem;
}
</style>
