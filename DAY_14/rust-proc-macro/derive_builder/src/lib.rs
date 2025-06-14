use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(Builder)]
pub fn derive_builder(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let struct_name = input.ident;
    let builder_name = syn::Ident::new(&format!("{}Builder", struct_name), struct_name.span());

    let fields = match input.data {
        syn::Data::Struct(data) => data.fields,
        _ => panic!("Builder can only be used with structs"),
    };

    // Extract field names and types
    let field_names: Vec<_> = fields.iter().map(|f| f.ident.as_ref().unwrap()).collect();
    let field_types: Vec<_> = fields.iter().map(|f| &f.ty).collect();

    let builder_fields = field_names
        .iter()
        .zip(field_types.iter())
        .map(|(name, ty)| {
            quote! { #name: Option<#ty> }
        });

    let setters = field_names
        .iter()
        .zip(field_types.iter())
        .map(|(name, ty)| {
            quote! {
                pub fn #name(mut self, #name: #ty) -> Self {
                    self.#name = Some(#name);
                    self
                }
            }
        });

    let build_fields = field_names.iter().map(|name| {
        quote! {
            #name: self.#name.ok_or_else(|| format!("{} is not set", stringify!(#name)))?
        }
    });

    let default_fields = field_names.iter().map(|name| {
        quote! { #name: None }
    });

    let expanded = quote! {
        pub struct #builder_name {
            #(#builder_fields,)*
        }

        impl #builder_name {
            #(#setters)*

            pub fn build(self) -> Result<#struct_name, Box<dyn std::error::Error>> {
                Ok(#struct_name {
                    #(#build_fields,)*
                })
            }
        }

        impl Default for #builder_name {
            fn default() -> Self {
                Self {
                    #(#default_fields,)*
                }
            }
        }
    };

    TokenStream::from(expanded)
}
