<template>
  <q-btn flat icon="more_vert">
    <q-menu>
      <q-list style="min-width: 100px" class="q-px-md">
        <q-item>
          <q-item-section thumbnail
            ><q-icon name="dark_mode"></q-icon
          ></q-item-section>
          <q-item-section side>
            <q-toggle
              v-model="darkToggleValue"
              @click="localSettingsStore.toggleDarkMode"
              label="Dark mode"
              left-label
              color="primary"
            />
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click="isLoginDialogShown += 1">
          <q-item-section thumbnail
            ><q-icon name="logout"></q-icon
          ></q-item-section>
          <q-item-section>Logout</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </q-btn>
  <LoginView :isDialogShown="isLoginDialogShown" />
</template>

<script setup lang="ts">
import LoginView from 'components/LoginView.vue';
import { ref, watch } from 'vue';
import { useQuasar } from 'quasar';
import { useLocalSettingsStore } from 'stores/local-settings-store';

const isLoginDialogShown = ref(0);

const $q = useQuasar();

const darkToggleValue = ref($q.dark.isActive);

const localSettingsStore = useLocalSettingsStore();

watch(
  () => $q.dark.isActive,
  () => {
    darkToggleValue.value = $q.dark.isActive;
    localSettingsStore.darkMode = $q.dark.isActive;
  }
);
</script>
