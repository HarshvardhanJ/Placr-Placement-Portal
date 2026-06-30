<template>
  <div class="card shadow-sm border-0 rounded-4 overflow-hidden">
    <div
      class="card-header bg-white border-bottom-0 d-flex justify-content-between align-items-center px-4 pt-4 pb-3"
    >
      <h3 class="card-title mb-0 fw-semibold">{{ title }}</h3>
      <slot name="header-actions" />
    </div>

    <div class="table-responsive">
      <table
        class="table table-vcenter card-table table-hover align-middle mb-0"
      >
        <thead>
          <tr>
            <th v-for="header in headers" :key="header.key">
              {{ header.label }}
            </th>
          </tr>
        </thead>

        <tbody v-if="rows.length">
          <tr v-for="(row, index) in rows" :key="index">
            <td v-for="header in headers" :key="header.key">
              <slot :name="header.key" :row="row">
                {{ row[header.key] }}
              </slot>
            </td>
          </tr>
        </tbody>

        <tbody v-else>
          <tr>
            <td :colspan="headers.length" class="empty-table">
              No data available.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  headers: Array,
  rows: Array,
});
</script>

<style scoped>
.table thead th {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748b;
  background: #f8fafc;
  border-bottom: 1px solid #e9ecef;
  padding: 0.95rem 1rem;
}

.table tbody td {
  vertical-align: middle;
  padding: 1rem;
}

.empty-table {
  padding: 3.25rem 1rem;
  text-align: center;
  color: #64748b;
  background: #fff;
}
</style>
