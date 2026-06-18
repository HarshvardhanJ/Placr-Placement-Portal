<template>
  <div class="dashboard-layout">
    <AppSidebar />

    <div class="dashboard-main">
      <AppTopbar />

      <main class="dashboard-content">
        <PageHeader
          title="Overview"
          subtitle="Real-time metrics and upcoming placement activities."
          :show-export="true"
          :show-create="true"
        >
          <template #actions>
            <button type="button" class="btn btn-primary">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="icon icon-tabler icons-tabler-outline icon-tabler-download"
              >
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2" />
                <path d="M7 11l5 5l5 -5" />
                <path d="M12 4l0 12" /></svg
              >Export
            </button>
          </template>
        </PageHeader>
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import AppSidebar from "@/components/shared/AppSidebar.vue";
import AppTopbar from "@/components/shared/AppTopbar.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

.dashboard-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f6f8fb;
}

.dashboard-content {
  flex: 1;
  padding: 1.5rem;
}
</style>
