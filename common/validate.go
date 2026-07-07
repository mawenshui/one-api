package common

import (
	"fmt"
	"strings"

	"github.com/go-playground/validator/v10"
)

var Validate *validator.Validate

func init() {
	Validate = validator.New()
}

// FormatValidationError turns a validator.ValidationErrors into a single
// human-readable string. Each field error becomes "字段: 原因".
//
// Why: previously the controller returned the generic
// "无效的输入，请检查您的输入" which gave the user no hint about
// which field was actually wrong. This helper makes the error
// self-explanatory.
func FormatValidationError(err error) string {
	if err == nil {
		return ""
	}
	if vErrs, ok := err.(validator.ValidationErrors); ok {
		parts := make([]string, 0, len(vErrs))
		for _, fe := range vErrs {
			parts = append(parts, fieldErrorMessage(fe))
		}
		return strings.Join(parts, "; ")
	}
	return err.Error()
}

// fieldErrorMessage turns one validator.FieldError into "字段名: 原因".
func fieldErrorMessage(fe validator.FieldError) string {
	field := fe.Field()
	// Translate struct field name to a friendlier label. The struct tag
	// `json:"username"` lets us read the JSON name for a nicer display.
	if fe.StructField() != "" {
		field = fe.StructField()
	}
	// If still empty, fall back to the field path.
	if field == "" {
		field = fe.Field()
	}
	switch fe.Tag() {
	case "required":
		return fmt.Sprintf("%s 是必填项", field)
	case "min":
		return fmt.Sprintf("%s 至少 %s 个字符", field, fe.Param())
	case "max":
		return fmt.Sprintf("%s 最多 %s 个字符", field, fe.Param())
	case "email":
		return fmt.Sprintf("%s 不是有效的邮箱地址", field)
	case "len":
		return fmt.Sprintf("%s 必须为 %s 个字符", field, fe.Param())
	case "oneof":
		return fmt.Sprintf("%s 必须是以下值之一: %s", field, fe.Param())
	default:
		return fmt.Sprintf("%s 不符合 %s 规则", field, fe.Tag())
	}
}
