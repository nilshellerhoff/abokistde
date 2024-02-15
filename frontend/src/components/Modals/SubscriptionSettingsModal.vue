<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <div class="text-h5">
          Settings for {{ subscription.publishing_channel.name }}
        </div>
      </q-card-section>
      <q-card-section>
        <table style="width: 100%">
          <tr>
            <td>Category</td>
            <td>
              <q-select
                name="Category"
                v-model="subscription.category_id"
                :options="contentStore.subscriptionCategories"
                option-label="name"
                option-value="id"
                emit-value
                map-options
                clearable
                placeholder="No category"
              />
            </td>
            <td>
              <q-btn flat round dense icon="add" @click="onAddCategoryClick" />
            </td>
          </tr>
        </table>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn color="negative" label="Remove" @click="onRemoveClick" />
        <q-btn
          color="primary"
          label="Save"
          :loading="isSaveLoading"
          @click="onSaveClick"
        />
        <q-btn color="primary" label="Cancel" @click="onDialogCancel" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { useDialogPluginComponent, useQuasar } from 'quasar';
import { useContentStore } from 'stores/content-store';
import { UserSubscription } from 'src/types/api';
import AddSubscriptionCategoryModal from 'components/Modals/AddSubscriptionCategoryModal.vue';
import { ref } from 'vue';

interface Props {
  subscriptionId: number;
}

const props = defineProps<Props>();

const $q = useQuasar();

const contentStore = useContentStore();

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

// this is part of our example (so not required)
const onSaveClick = () => {
  isSaveLoading.value = true;
  contentStore
    .updateSubscription(subscription.id, {
      publishing_channel_id: subscription.publishing_channel_id,
      category_id: subscription.category_id,
    })
    .then(() => {
      onDialogOK();
    })
    .catch(() => {
      $q.notify({
        type: 'negative',
        message: 'Failed to save settings',
      });
    })
    .finally(() => {
      isSaveLoading.value = false;
    });
  // on OK, it is REQUIRED to
  // call onDialogOK (with optional payload)
  // or with payload: onDialogOK({ ... })
  // ...and it will also hide the dialog automatically
};

const onRemoveClick = () => {
  if (
    confirm(
      `Remove ${subscription.publishing_channel.name} from subscriptions?`
    )
  ) {
    contentStore.removeSubscription(subscription.id);
    onDialogOK();
  }
};

const onAddCategoryClick = () => {
  $q.dialog({
    component: AddSubscriptionCategoryModal,
  });
};

const subscription = contentStore.getSubscriptionById(
  props.subscriptionId
) as UserSubscription;
</script>
