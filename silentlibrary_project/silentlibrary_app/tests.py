from django.test import TestCase
from .models import Publisher

# Create your tests here.
class PublisherTestCase(TestCase):

    def test_create_publisher(self):
        publisher = Publisher.objects.create(name="Test Publisher", address="123 Test St")
        self.assertEqual(publisher.name, "Test Publisher")
        self.assertEqual(publisher.address, "123 Test St")

    def test_update_publisher(self):
        publisher = Publisher.objects.create(name="Test Publisher", address="123 Test St")
        publisher.name = "Updated Publisher"
        publisher.address = "456 Updated St"
        publisher.save()

        updated_publisher = Publisher.objects.get(pk=publisher.pk)
        self.assertEqual(updated_publisher.name, "Updated Publisher")
        self.assertEqual(updated_publisher.address, "456 Updated St")

    def test_delete_publisher(self):
        publisher = Publisher.objects.create(name="Test Publisher", address="123 Test St")
        publisher.delete()
        with self.assertRaises(Publisher.DoesNotExist):
            Publisher.objects.get(name="Test Publisher")
