from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ('id', 'date', 'customer_name', 'invoice_details')

    def create(self, validated_data):
        invoice_details_data = validated_data.pop('invoice_details')
        invoice = Invoice.objects.create(**validated_data)
        InvoiceDetail.objects.bulk_create([
            InvoiceDetail(invoice=invoice, **detail_data)
            for detail_data in invoice_details_data
        ])
        return invoice

    def update(self, instance, validated_data):
        invoice_details_data = validated_data.pop('invoice_details')
        instance.invoice_details.all().delete()
        InvoiceDetail.objects.bulk_create([
            InvoiceDetail(invoice=instance, **detail_data)
            for detail_data in invoice_details_data
        ])
        return super().update(instance, validated_data)