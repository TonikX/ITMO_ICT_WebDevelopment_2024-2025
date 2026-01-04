import { mergeProps as _mergeProps, createVNode as _createVNode, createElementVNode as _createElementVNode } from "vue";
// Components
import { VTextField } from "../VTextField/index.js"; // Composables
import { useTextColor } from "../../composables/color.js";
import { forwardRefs } from "../../composables/forwardRefs.js"; // Utilities
import { ref, shallowRef } from 'vue';
import { genericComponent, propsFactory, useRender } from "../../util/index.js"; // Types
export const makeVTimePickerFieldProps = propsFactory({
  active: Boolean,
  color: String,
  disabled: Boolean,
  label: String,
  modelValue: String,
  readonly: Boolean
}, 'VTimePickerField');
export const VTimePickerField = genericComponent()({
  name: 'VTimePickerField',
  inheritAttrs: false,
  props: makeVTimePickerFieldProps(),
  emits: {
    'update:modelValue': v => true
  },
  setup(props, _ref) {
    let {
      emit,
      attrs
    } = _ref;
    const {
      textColorClasses,
      textColorStyles
    } = useTextColor(() => props.color);
    const vTextInputRef = ref();
    const isFocused = shallowRef(false);
    function onKeydown(e) {
      if (['Backspace', 'Delete'].includes(e.key)) {
        e.preventDefault();
        const target = e.target;
        target.value = '';
        emit('update:modelValue', null);
      }
    }
    useRender(() => {
      return _createElementVNode("div", null, [_createVNode(VTextField, _mergeProps({
        "ref": vTextInputRef,
        "_as": "VTimePickerField",
        "autocomplete": "off",
        "class": ['v-time-picker-controls__time__field', {
          'v-time-picker-controls__time__field--active': props.active
        }, props.active ? textColorClasses.value : []],
        "style": props.active ? textColorStyles.value : [],
        "disabled": props.disabled,
        "variant": "solo-filled",
        "inputmode": "numeric",
        "hideDetails": true,
        "flat": true,
        "modelValue": props.modelValue ?? (isFocused.value ? '' : '--'),
        "onUpdate:modelValue": v => emit('update:modelValue', v),
        "onKeydown": onKeydown,
        "onFocus": () => isFocused.value = true,
        "onBlur": () => isFocused.value = false
      }, attrs), null), _createElementVNode("div", {
        "class": "v-time-picker-controls__field-label"
      }, [props.label])]);
    });
    return forwardRefs({}, vTextInputRef);
  }
});
//# sourceMappingURL=VTimePickerField.js.map