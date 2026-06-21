<template>
  <div class="card shadow-sm">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h3 class="card-title mb-0">{{ title }}</h3>
    </div>

    <div class="table-responsive">
      <table class="table table-vcenter card-table table-hover">
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
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #6b7280;
  background: #f8fafc;
  border-bottom: 1px solid #e9ecef;
}

.table tbody td {
  vertical-align: middle;
}

.empty-table {
  padding: 3rem;
  text-align: center;
  color: #6c757d;
}
</style>
