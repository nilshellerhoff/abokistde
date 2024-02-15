<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <div class="text-h5">Add a subscription category</div>
      </q-card-section>
      <q-card-section>
        <table style="width: 100%">
          <tr>
            <td>Name</td>
            <td>
              <q-input v-model="categoryName" />
            </td>
          </tr>
        </table>
      </q-card-section>

      <!-- buttons example -->
      <q-card-actions align="right">
        <q-btn
          color="primary"
          label="Save"
          @click="onSaveClick"
          :disable="!categoryName"
          :loading="isSaveLoading"
        />
        <q-btn color="primary" label="Cancel" @click="onDialogCancel" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { useDialogPluginComponent, useQuasar } from 'quasar';
import { useContentStore } from 'stores/content-store';
import { ref } from 'vue';

const $q = useQuasar();

defineEmits([
  // REQUIRED; need to specify some events that your
  // component will emit through useDialogPluginComponent()
  ...useDialogPluginComponent.emits,
]);

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();
// dialogRef      - Vue ref to be applied to QDialog
// onDialogHide   - Function to be used as handler for @hide on QDialog
// onDialogOK     - Function to call to settle dialog with "ok" outcome
//                    example: onDialogOK() - no payload
//                    example: onDialogOK({ /*...*/ }) - with payload
// onDialogCancel - Function to call to settle dialog with "cancel" outcome

const isSaveLoading = ref(false);

const onSaveClick = () => {
  if (!categoryName.value) {
    return;
  }
  isSaveLoading.value = true;
  contentStore
    .addSubscriptionCategory({
      name: categoryName.value,
    })
    .then(() => {
      onDialogOK();
    })
    .catch((error) => {
      console.error(error);
      $q.notify({
        type: 'negative',
        message: 'Error adding subscription category',
      });
    })
    .finally(() => {
      isSaveLoading.value = false;
    });
};

const categoryName = ref(null);

const contentStore = useContentStore();
</script>
