<template>
  <q-dialog :persistent="!isLoggedIn" v-model="isDialogShownLocal">
    <q-card :style="{ backgroundColor: '#fff', width: '500px' }">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">{{ isLoggedIn ? 'Log out' : 'Log in' }}</div>
        <q-space />
        <q-btn
          v-if="isLoggedIn"
          icon="close"
          flat
          round
          dense
          @click="isDialogShownLocal = false"
        />
      </q-card-section>

      <q-card-section>
        <iframe
          style="border: 0; width: 100%; height: 400px"
          :src="loginUrl"
          @load="checkLogin(true)"
        ></iframe>
      </q-card-section>
      <div class="q-pa-sm" style="width: 500px">
        <abokistde-logo class="q-ma-auto" />
      </div>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { apiClient } from 'src/util/api';
import { getLoginUrl } from 'src/util/host';
import AbokistdeLogo from 'components/AbokistdeLogo.vue';

interface Props {
  isDialogShown: number;
}

const props = defineProps<Props>();

const isLoggedIn = ref(false);
const isDialogShownLocal = ref(false);

const checkLogin = (reloadPage = false) => {
  apiClient
    .get('/episode/?limit=1')
    .then(() => {
      const oldIsLoggedIn = isLoggedIn.value;
      isLoggedIn.value = true;
      console.log('Logged in');
      if (oldIsLoggedIn !== isLoggedIn.value && reloadPage) {
        window.location.reload();
        isDialogShownLocal.value = false;
      }
    })
    .catch(() => {
      isLoggedIn.value = false;
      isDialogShownLocal.value = true;
      console.log('Not logged in');
    });
};

checkLogin();

const loginUrl = getLoginUrl();

watch(
  () => props.isDialogShown,
  () => {
    isDialogShownLocal.value = true;
    console.log('isDialogShown changed to ' + isDialogShownLocal.value);
  }
);
</script>

<style>
.q-dialog__backdrop {
  backdrop-filter: blur(20px);
}
</style>
