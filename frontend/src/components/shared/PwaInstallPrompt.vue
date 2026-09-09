<template>
  <div v-if="canInstall" class="pwa-install shadow-sm" role="status">
    <div class="pwa-copy">
      <strong>Install PLACR</strong>
      <span>Open faster from your home screen.</span>
    </div>
    <div class="d-flex align-items-center gap-2">
      <button type="button" class="btn btn-sm btn-primary" @click="install">
        <i class="ti ti-device-mobile-down me-1"></i>
        Install
      </button>
      <button
        type="button"
        class="btn btn-sm btn-outline-secondary pwa-dismiss"
        aria-label="Dismiss install prompt"
        @click="dismiss"
      >
        <i class="ti ti-x"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const canInstall = ref(false);
const deferredPrompt = ref(null);

const dismissedKey = "placr-pwa-install-dismissed";

const handleBeforeInstallPrompt = (event) => {
  if (localStorage.getItem(dismissedKey) === "1") return;
  event.preventDefault();
  deferredPrompt.value = event;
  canInstall.value = true;
};

const install = async () => {
  if (!deferredPrompt.value) return;
  deferredPrompt.value.prompt();
  await deferredPrompt.value.userChoice;
  deferredPrompt.value = null;
  canInstall.value = false;
};

const dismiss = () => {
  localStorage.setItem(dismissedKey, "1");
  deferredPrompt.value = null;
  canInstall.value = false;
};

onMounted(() => {
  window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
  window.addEventListener("appinstalled", dismiss);
});

onBeforeUnmount(() => {
  window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
  window.removeEventListener("appinstalled", dismiss);
});
</script>

<style scoped>
.pwa-install {
  position: fixed;
  right: 1rem;
  bottom: 1rem;
  z-index: 1080;
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: min(420px, calc(100vw - 2rem));
  padding: 0.85rem;
  border: 1px solid #dbe4f0;
  border-radius: 8px;
  background: #fff;
}

.pwa-copy {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.pwa-copy span {
  color: #64748b;
  font-size: 0.875rem;
}

.pwa-dismiss {
  width: 32px;
  height: 32px;
  display: inline-grid;
  place-items: center;
  padding: 0;
}

@media (max-width: 575.98px) {
  .pwa-install {
    right: 0.75rem;
    bottom: 0.75rem;
    left: 0.75rem;
    max-width: none;
  }
}
</style>
