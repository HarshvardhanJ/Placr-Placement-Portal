<template>
  <div v-if="show" class="modal d-block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Company Details</h5>

          <button class="btn-close" @click="emit('close')" />
        </div>

        <div class="modal-body">
          <!-- details go here -->
          <div class="row g-3">
            <div class="col-md-6">
              <label class="text-secondary">Company Name</label>
              <div class="fw-medium">
                {{ company?.name }}
              </div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">Industry</label>
              <div class="fw-medium">
                {{ company?.industry }}
              </div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">HR Name</label>
              <div class="fw-medium">
                {{ company?.hr_name }}
              </div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">Email</label>
              <div class="fw-medium">
                {{ company?.email }}
              </div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">Status</label>
              <div class="fw-medium">
                {{ company?.status }}
              </div>
            </div>

            <div class="col-md-6">
              <label class="text-secondary">Total Drives</label>
              <div class="fw-medium">
                {{ company?.drives }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-if="show" class="modal-backdrop fade show" />
</template>
<script setup>
const props = defineProps({
  company: {
    type: Object,
    default: null,
  },
  show: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close"]);
</script>
