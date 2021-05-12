# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime
from nose2.tools import such
import tempfile
from pathlib import Path

from . import app, get_random_str
from qai_testbed_backend.usecases.inventory import InventoryService
from qai_testbed_backend.controllers.dto.inventory import PutInventoryReq, AppendInventoryReq
from qai_testbed_backend.across.exception import QAIException, QAINotFoundException, QAIInvalidRequestException


with such.A('inventories') as it:

    with it.having('GET /inventories'):
        @it.should('should return I12000.')
        def test():
            with app.app_context():
                response = InventoryService().get_inventories(organizer_id='dep-a', ml_component_id=1)
                it.assertEqual(response.result.code, 'I12000')

        @it.should('should return I14000 if `organizer_id` is not found.')
        def test():
            with app.app_context():
                try:
                    InventoryService().get_inventories(organizer_id='hoge',  # invalid
                                                       ml_component_id=1)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'I14000')

        @it.should('should return I14000 if `ml_component_id` is not found.')
        def test():
            with app.app_context():
                try:
                    InventoryService().get_inventories(organizer_id='dep-a',
                                                       ml_component_id=999)  # invalid
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'I14000')

        @it.should('should return inventories.')
        def test():
            with app.app_context():
                response = InventoryService().get_inventories(organizer_id='dep-a', ml_component_id=1)
                it.assertGreaterEqual(len(response.inventories), 1)
                for i in response.inventories:
                    it.assertTrue(type(i.id_) is int)
                    it.assertNotEqual(i.id_, 0)
                    it.assertTrue(type(i.name) is str)
                    it.assertNotEqual(i.name, '')
                    it.assertTrue(type(i.type.id_) is int)
                    it.assertNotEqual(i.type.id_, 0)
                    it.assertTrue(type(i.type.name) is str)
                    it.assertNotEqual(i.type.name, '')
                    it.assertTrue(type(i.file_system.id_) is int)
                    it.assertNotEqual(i.file_system.id_, 0)
                    it.assertTrue(type(i.file_system.name) is str)
                    it.assertNotEqual(i.file_system.name, '')
                    it.assertTrue(type(i.description) is str)
                    it.assertNotEqual(i.description, '')
                    it.assertTrue(type(i.schema) is str)
                    it.assertNotEqual(i.schema, '')
                    it.assertTrue(type(i.formats) is list)
                    for f in i.formats:
                        it.assertTrue(type(f.id) is int)
                        it.assertNotEqual(f.id, 0)
                        it.assertTrue(type(f.type) is str)
                        it.assertNotEqual(f.type, '')
                        it.assertTrue(type(f.format) is str)
                    it.assertNotEqual(f.format, '')
                    it.assertTrue(type(i.file_path) is str)
                    it.assertNotEqual(i.file_path, '')
                    it.assertTrue(type(i.creation_datetime) is datetime)
                    it.assertNotEqual(i.creation_datetime, None)
                    it.assertTrue(type(i.update_datetime) is datetime)
                    it.assertNotEqual(i.update_datetime, None)

    with it.having('POST /inventories'):
        @it.should('should return I22000.')
        def test():
            with tempfile.TemporaryDirectory() as dir_name:
                file_name = str(Path(dir_name) / 'test.csv')
                with open(file_name, "w") as f:
                    f.write('test1,test2')
                req = AppendInventoryReq(name='Testdata99',
                                         type_id=1,
                                         file_system_id=2,
                                         file_path=file_name,
                                         description='テスト99用のデータ',
                                         formats=['csv', 'zip'],
                                         schema='http://sample.com/datafotmat/testdata2')
                with app.app_context():
                    response = InventoryService().append_inventory(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.assertEqual(response.result.code, 'I22000')

        @it.should('should return I24001 if invalid file path is not start alphabet for WINDOWS_FILE.')
        def test():
            req = AppendInventoryReq(name='Testdata99',
                                     type_id=1,
                                     file_system_id=2,
                                     file_path='/mnt/xxx/99',
                                     description='テスト99用のデータ',
                                     formats=['csv', 'zip'],
                                     schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().append_inventory(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I24001')

        @it.should('should return I24001 if invalid file path is too long for WINDOWS_FILE.')
        def test():
            req = AppendInventoryReq(name='Testdata99',
                                     type_id=1,
                                     file_system_id=2,
                                     file_path='C:\\'+get_random_str(257),
                                     description='テスト99用のデータ',
                                     formats=['csv', 'zip'],
                                     schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().append_inventory(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I24001')

        @it.should('should return I24001 if invalid file path is not start slash for UNIX_FILE_SYSTEM.')
        def test():
            req = AppendInventoryReq(name='Testdata99',
                                     type_id=1,
                                     file_system_id=1,
                                     file_path='mnt/xxx/99',
                                     description='テスト99用のデータ',
                                     formats=['csv', 'zip'],
                                     schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().append_inventory(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I24001')

        @it.should('should return I24001 if invalid file item path is too long for UNIX_FILE_SYSTEM.')
        def test():
            req = AppendInventoryReq(name='Testdata99',
                                     type_id=1,
                                     file_system_id=1,
                                     file_path='/'+get_random_str(255)+'/'+get_random_str(256),
                                     description='テスト99用のデータ',
                                     formats=['csv', 'zip'],
                                     schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().append_inventory(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I24001')

        @it.should('should return I24001 if invalid file path is too long for UNIX_FILE_SYSTEM.')
        def test():
            file_path = ''
            for i in range(8):
                file_path = file_path + '/' + get_random_str(127)
            req = AppendInventoryReq(name='Testdata99',
                                     type_id=1,
                                     file_system_id=1,
                                     file_path=file_path,
                                     description='テスト99用のデータ',
                                     formats=['csv', 'zip'],
                                     schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().append_inventory(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I24001')

        @it.should('should return I24001 if invalid file_system_id.')
        def test():
            req = AppendInventoryReq(name='Testdata99',
                                     type_id=1,
                                     file_system_id=999,
                                     file_path='/aaa',
                                     description='テスト99用のデータ',
                                     formats=['csv', 'zip'],
                                     schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().append_inventory(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I24001')

        @it.should('should return I24000 if file_path not found.')
        def test():
            req = AppendInventoryReq(name='Testdata99',
                                     type_id=1,
                                     file_system_id=2,
                                     file_path='C:\\'+get_random_str(64),
                                     description='テスト99用のデータ',
                                     formats=['csv', 'zip'],
                                     schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().append_inventory(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'I24000')

    with it.having('PUT /inventories'):
        @it.should('should return I32000.')
        def test():
            with tempfile.TemporaryDirectory() as dir_name:
                file_name = str(Path(dir_name) / 'test.csv')
                with open(file_name, "w") as f:
                    f.write('test1,test2')
                append_req = AppendInventoryReq(name='case1',
                                                type_id=1,
                                                file_system_id=2,
                                                file_path=file_name,
                                                description='追加データ',
                                                formats=['csv', 'zip'],
                                                schema='http://sample.com/datafotmat/testdata2')
                put_req = PutInventoryReq(name='case1',
                                          type_id=1,
                                          file_system_id=2,
                                          file_path=file_name,
                                          description='更新データ',
                                          formats=['csv', 'zip'],
                                          schema='http://sample.com/datafotmat/testdata2')
                with app.app_context():
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=1,
                                                        req=append_req)

                    response = InventoryService().get_inventories(organizer_id='dep-a', ml_component_id=1)
                    append_inv = response.inventories[-1]

                    response = InventoryService().put_inventory(organizer_id='dep-a', ml_component_id=1,
                                                                inventory_id=append_inv.id_, req=put_req)
                    it.assertEqual(response.result.code, 'I32000')

        @it.should('should return I34000 if inventory_id is not found.')
        def test():
            req = PutInventoryReq(name='Testdata99',
                                  type_id=1,
                                  file_system_id=1,
                                  file_path='/mnt/xxx/99',
                                  description='テスト99用のデータ',
                                  formats=['csv', 'zip'],
                                  schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().put_inventory(organizer_id='dep-a',
                                                     ml_component_id=1,
                                                     inventory_id=999,  # invalid inventory_id
                                                     req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'I34000')

        @it.should('should return I34000 if file_path not found.')
        def test():
            req = PutInventoryReq(name='Testdata99',
                                  type_id=1,
                                  file_system_id=2,
                                  file_path='C:\\'+get_random_str(64),
                                  description='テスト99用のデータ',
                                  formats=['csv', 'zip'],
                                  schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().put_inventory(organizer_id='dep-a', ml_component_id=1, inventory_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'I34000')

        @it.should('should return I34001 if inventory was deleted.')
        def test():
            with tempfile.TemporaryDirectory() as dir_name:
                file_name = str(Path(dir_name) / 'test.csv')
                with open(file_name, "w") as f:
                    f.write('test1,test2')
                append_req = AppendInventoryReq(name='Testdata_Append1',
                                                type_id=1,
                                                file_system_id=2,
                                                file_path=file_name,
                                                description='追加→削除データ',
                                                formats=['csv', 'zip'],
                                                schema='http://sample.com/datafotmat/testdata2')
                req = PutInventoryReq(name='Testdata99',
                                      type_id=1,
                                      file_system_id=1,
                                      file_path='/mnt/xxx/99',
                                      description='テスト99用のデータ',
                                      formats=['csv', 'zip'],
                                      schema='http://sample.com/datafotmat/testdata2')
                with app.app_context():
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=1,
                                                        req=append_req)

                    response = InventoryService().get_inventories(organizer_id='dep-a', ml_component_id=1)
                    append_inv = response.inventories[-1]

                    InventoryService().delete_inventory(organizer_id='dep-a', ml_component_id=1,
                                                        inventory_id=append_inv.id_)

                    try:
                        InventoryService().put_inventory(organizer_id='dep-a',
                                                         ml_component_id=1,
                                                         inventory_id=append_inv.id_,  # delete inventory_id
                                                         req=req)
                        it.fail()
                    except QAIException as e:
                        it.assertTrue(type(e) is QAINotFoundException)
                        it.assertEqual(e.result_code, 'I34001')


        @it.should('should change update_datetime if edit inventory')
        def test():
            with tempfile.TemporaryDirectory() as dir_name:
                file_name1 = str(Path(dir_name) / 'test1.csv')
                with open(file_name1, "w") as f:
                    f.write('test1,test2')
                file_name2 = str(Path(dir_name) / 'test2.csv')
                with open(file_name2, "w") as f:
                    f.write('test3,test4')

                append_req = AppendInventoryReq(name='Testdata_Append1',
                                                type_id=1,
                                                file_system_id=2,
                                                file_path=file_name1,
                                                description='追加→削除データ',
                                                formats=['csv', 'zip'],
                                                schema='http://sample.com/datafotmat/testdata2')
                edit_req = PutInventoryReq(name='Testdata99',
                                           type_id=1,
                                           file_system_id=2,
                                           file_path=file_name2,
                                           description='テスト99用のデータ',
                                           formats=['csv', 'zip', 'json'],
                                           schema='http://sample.com/datafotmat/testdata2-2')
                with app.app_context():
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=1,
                                                        req=append_req)

                    response = InventoryService().get_inventories(organizer_id='dep-a', ml_component_id=1)
                    append_inv = response.inventories[-1]

                    InventoryService().put_inventory(organizer_id='dep-a',
                                                     ml_component_id=1,
                                                     inventory_id=append_inv.id_,
                                                     req=edit_req)

                    response = InventoryService().get_inventories(organizer_id='dep-a', ml_component_id=1)
                    edit_inv = response.inventories[-1]

                    it.assertEqual(append_inv.id_, edit_inv.id_)
                    it.assertEqual(append_inv.creation_datetime, edit_inv.creation_datetime)
                    it.assertNotEqual(append_inv.update_datetime, edit_inv.update_datetime)
                    it.assertEqual(edit_inv.file_path, edit_req.file_path)
                    it.assertEqual(edit_inv.type.id_, edit_req.type_id)
                    it.assertEqual(edit_inv.file_system.id_, edit_req.file_system_id)
                    it.assertEqual(edit_inv.name, edit_req.name)
                    it.assertEqual([f.format for f in edit_inv.formats], edit_req.formats)

        @it.should('should return I34002 if invalid file path is not start alphabet for WINDOWS_FILE.')
        def test():
            req = PutInventoryReq(name='Testdata99',
                                  type_id=1,
                                  file_system_id=2,
                                  file_path='/mnt/xxx/99',
                                  description='テスト99用のデータ',
                                  formats=['csv', 'zip'],
                                  schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().put_inventory(organizer_id='dep-a', ml_component_id=1,
                                                     inventory_id=1,
                                                     req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I34002')

        @it.should('should return I34002 if invalid file path is too long for WINDOWS_FILE.')
        def test():
            req = PutInventoryReq(name='Testdata99',
                                  type_id=1,
                                  file_system_id=2,
                                  file_path='C:\\'+get_random_str(257),
                                  description='テスト99用のデータ',
                                  formats=['csv', 'zip'],
                                  schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().put_inventory(organizer_id='dep-a', ml_component_id=1,
                                                     inventory_id=1,
                                                     req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I34002')

        @it.should('should return I34002 if invalid file path is not start slash for UNIX_FILE_SYSTEM.')
        def test():
            req = PutInventoryReq(name='Testdata99',
                                  type_id=1,
                                  file_system_id=1,
                                  file_path='mnt/xxx/99',
                                  description='テスト99用のデータ',
                                  formats=['csv', 'zip'],
                                  schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().put_inventory(organizer_id='dep-a', ml_component_id=1,
                                                     inventory_id=1,
                                                     req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I34002')

        @it.should('should return I34002 if invalid file item path is too long for UNIX_FILE_SYSTEM.')
        def test():
            req = PutInventoryReq(name='Testdata99',
                                  type_id=1,
                                  file_system_id=1,
                                  file_path='/'+get_random_str(255)+'/'+get_random_str(256),
                                  description='テスト99用のデータ',
                                  formats=['csv', 'zip'],
                                  schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().put_inventory(organizer_id='dep-a', ml_component_id=1,
                                                     inventory_id=1,
                                                     req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I34002')

        @it.should('should return I34002 if invalid file path is too long for UNIX_FILE_SYSTEM.')
        def test():
            file_path = ''
            for i in range(8):
                file_path = file_path + '/' + get_random_str(127)
            req = PutInventoryReq(name='Testdata99',
                                  type_id=1,
                                  file_system_id=1,
                                  file_path=file_path,
                                  description='テスト99用のデータ',
                                  formats=['csv', 'zip'],
                                  schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().put_inventory(organizer_id='dep-a', ml_component_id=1,
                                                     inventory_id=1,
                                                     req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I34002')

        @it.should('should return I34002 if invalid file_system_id.')
        def test():
            req = PutInventoryReq(name='Testdata99',
                                  type_id=1,
                                  file_system_id=999,
                                  file_path='/aaa',
                                  description='テスト99用のデータ',
                                  formats=['csv', 'zip'],
                                  schema='http://sample.com/datafotmat/testdata2')
            with app.app_context():
                try:
                    InventoryService().put_inventory(organizer_id='dep-a', ml_component_id=1,
                                                     inventory_id=1,
                                                     req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'I34002')

it.createTests(globals())
