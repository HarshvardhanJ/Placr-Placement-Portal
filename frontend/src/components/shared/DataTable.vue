<template>
  <div class="card shadow-sm">
    <div class="card-header">
      <h3 class="card-title">Upcoming Drives</h3>
    </div>

    <div class="table-responsive">
      <table class="table card-table table-vcenter">
        <thead>
          <tr>
            <th v-for="header in headers" :key="header.key">
              {{ header.label }}
            </th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(row, index) in rows" :key="index">
            <td v-for="header in headers" :key="header.key">
              <slot :name="header.key" :row="row">
                {{ row[header.key] }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  headers: Array,
  rows: Array,
});
</script>
