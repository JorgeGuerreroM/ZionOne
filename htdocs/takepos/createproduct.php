<?php
/* Copyright (C) 2018 Andreu Bisquerra	<jove@bisquerra.com>
 * Copyright (C) 2020 Laurent Destailleur  <eldy@users.sourceforge.net>
 * Copyright (C) 2024       Frédéric France         <frederic.france@free.fr>
 * Copyright (C) 2025		Custom Development		<custom@development.local>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

/**
 *	\file       htdocs/takepos/createproduct.php
 *	\ingroup    takepos
 *	\brief      Popup to create a new product from TakePos
 */

if (!defined('NOTOKENRENEWAL')) {
	define('NOTOKENRENEWAL', '1');
}
if (!defined('NOREQUIREMENU')) {
	define('NOREQUIREMENU', '1');
}
if (!defined('NOREQUIREHTML')) {
	define('NOREQUIREHTML', '1');
}
if (!defined('NOREQUIREAJAX')) {
	define('NOREQUIREAJAX', '1');
}

// Load Dolibarr environment
require '../main.inc.php'; // Load $user and permissions
require_once DOL_DOCUMENT_ROOT.'/core/lib/functions.lib.php';
require_once DOL_DOCUMENT_ROOT.'/product/class/product.class.php';
require_once DOL_DOCUMENT_ROOT.'/categories/class/categorie.class.php';
require_once DOL_DOCUMENT_ROOT.'/core/modules/product/modules_product.class.php';
if (isModEnabled('barcode')) {
	require_once DOL_DOCUMENT_ROOT.'/core/modules/barcode/modules_barcode.class.php';
}

global $mysoc;
/**
 * @var Conf $conf
 * @var DoliDB $db
 * @var HookManager $hookmanager
 * @var Societe $mysoc
 * @var Translate $langs
 * @var User $user
 */

$langs->loadLangs(array("products", "takepos", "cashdesk"));

$place = (GETPOST('place', 'aZ09') ? GETPOST('place', 'aZ09') : '0');
$action = GETPOST('action', 'aZ09');

if (!$user->hasRight('takepos', 'run') || !$user->hasRight('produit', 'creer')) {
	accessforbidden();
}

// Handle product creation
if ($action == 'add' && $user->hasRight('produit', 'creer')) {
	$error = 0;
	$errors = array();
	
	$label = GETPOST('label', 'alphanohtml');
	$price = GETPOSTFLOAT('price');
	$ref = GETPOST('ref', 'alpha');
	$barcode = GETPOST('barcode', 'alpha');
	$type = GETPOSTINT('type'); // 0 = product, 1 = service
	$category = GETPOSTINT('category');
	
	if (empty($label)) {
		$error++;
		$errors[] = $langs->trans('ErrorFieldRequired', $langs->transnoentities('Label'));
	}
	
	if (empty($ref)) {
		// Auto-generate reference if needed
		$module = getDolGlobalString('PRODUCT_CODEPRODUCT_ADDON', 'mod_codeproduct_leopard');
		if (substr($module, 0, 16) == 'mod_codeproduct_' && substr($module, -3) == 'php') {
			$module = substr($module, 0, dol_strlen($module) - 4);
		}
		$result = dol_include_once('/core/modules/product/'.$module.'.php');
		if ($result > 0) {
			$modCodeProduct = new $module();
			if ($modCodeProduct->code_auto) {
				$ref = $modCodeProduct->getNextValue(null, $type);
			}
		}
		
		if (empty($ref)) {
			$error++;
			$errors[] = $langs->trans('ErrorFieldRequired', $langs->transnoentities('ProductRef'));
		}
	}
	
	if (!$error) {
		// Check if ref already exists
		$product_test = new Product($db);
		$result_test = $product_test->fetch('', $ref);
		if ($result_test > 0) {
			$error++;
			$errors[] = $langs->trans('ProductAlreadyExists', $ref);
		}
		
		// Check if barcode already exists (if provided)
		if (!empty($barcode)) {
			$sql = "SELECT rowid FROM ".MAIN_DB_PREFIX."product WHERE barcode = '".$db->escape($barcode)."'";
			$resql = $db->query($sql);
			if ($resql && $db->num_rows($resql) > 0) {
				$error++;
				$errors[] = $langs->trans('BarcodeAlreadyExists', $barcode);
			}
		}
	}
	
	if (!$error) {
		$product = new Product($db);
		$product->ref = $ref;
		$product->label = $label;
		$product->type = $type;
		$product->price = ($price > 0) ? $price : 0;
		$product->price_base_type = 'HT';
		$product->tva_tx = getDolGlobalFloat('TAKEPOS_DEFAULT_VAT_RATE', 0);
		$product->status = 1; // For sale
		$product->status_buy = 0; // Not for purchase by default
		$product->fk_product_type = $type;
		
		// Add barcode if provided or auto-generate if configured
		if (!empty($barcode)) {
			$product->barcode = $barcode;
			$product->barcode_type = getDolGlobalInt('PRODUIT_DEFAULT_BARCODE_TYPE', 0);
		} elseif (getDolGlobalString('BARCODE_PRODUCT_ADDON_NUM') && getDolGlobalString('PRODUIT_DEFAULT_BARCODE_TYPE')) {
			// Auto-generate barcode if configured
			$modBarCodeProduct = null;
			$module = getDolGlobalString('BARCODE_PRODUCT_ADDON_NUM', 'mod_barcode_product_standard');
			if (substr($module, 0, 15) == 'mod_barcode_product_' && substr($module, -3) == 'php') {
				$module = substr($module, 0, dol_strlen($module) - 4);
			}
			$result_barcode = dol_include_once('/core/modules/barcode/'.$module.'.php');
			if ($result_barcode > 0) {
				$modBarCodeProduct = new $module();
				if ($modBarCodeProduct->code_auto) {
					$auto_barcode = $modBarCodeProduct->getNextValue($product, getDolGlobalInt('PRODUIT_DEFAULT_BARCODE_TYPE'));
					if ($auto_barcode) {
						$product->barcode = $auto_barcode;
						$product->barcode_type = getDolGlobalInt('PRODUIT_DEFAULT_BARCODE_TYPE', 0);
					}
				}
			}
		}
		
		$result = $product->create($user);
		
		if ($result > 0) {
			// Add to category if specified
			if ($category > 0) {
				$cat = new Categorie($db);
				$cat->fetch($category);
				$cat->add_type($product, 'product');
			}
			
			// Return success message and refresh products
			echo '<script>
				alert("'.dol_escape_js($langs->trans('ProductCreatedSuccessfully', $product->ref)).'");
				if (parent.LoadProducts) {
					parent.LoadProducts(0); // Refresh products in TakePos
				}
				parent.$.colorbox.close();
			</script>';
			exit;
		} else {
			$error++;
			$errors[] = $product->error;
		}
	}
}

// Get categories for the select dropdown
$categories = array();
$categorie = new Categorie($db);
$allcategories = $categorie->get_full_arbo('product', ((getDolGlobalInt('TAKEPOS_ROOT_CATEGORY_ID') > 0) ? getDolGlobalInt('TAKEPOS_ROOT_CATEGORY_ID') : 0), 1);

/*
 * View
 */

$arrayofcss = array('/takepos/css/pos.css.php');
$arrayofjs = array();

top_htmlhead('', '', 0, 0, $arrayofjs, $arrayofcss);
?>
<body>

<script>
	/**
	 * Save (validate)
	 */
	function Save() {
		// Basic validation
		if (jQuery('#label').val() == '') {
			alert('<?php echo dol_escape_js($langs->trans('ErrorFieldRequired', $langs->transnoentities('Label'))); ?>');
			return false;
		}
		
		console.log("Creating new product with label="+jQuery("#label").val());
		return true; // Allow form submission
	}

	jQuery(document).ready(function() {
		jQuery('#label').focus();
	});
</script>

<br>
<center>

<?php
// Display errors
if (!empty($errors)) {
	foreach ($errors as $error) {
		print '<div class="error">'.$error.'</div><br>';
	}
}
?>

<form name="createproductform" method="POST" action="<?php echo $_SERVER["PHP_SELF"]; ?>">
	<input type="hidden" name="token" value="<?php echo newToken(); ?>">
	<input type="hidden" name="action" value="add">
	<input type="hidden" name="place" value="<?php echo dol_escape_htmltag($place); ?>">
	
	<table>
		<tr>
			<td><strong><?php echo $langs->trans('Label'); ?> *:</strong></td>
			<td><input type="text" id="label" name="label" class="takepospay" style="width:300px;" placeholder="<?php echo dol_escape_htmltag($langs->trans('ProductName')); ?>" value="<?php echo dol_escape_htmltag(GETPOST('label', 'alphanohtml')); ?>"></td>
		</tr>
		<tr>
			<td><strong><?php echo $langs->trans('ProductRef'); ?>:</strong></td>
			<td><input type="text" id="ref" name="ref" class="takepospay" style="width:200px;" placeholder="<?php echo dol_escape_htmltag($langs->trans('Reference')); ?>" value="<?php echo dol_escape_htmltag(GETPOST('ref', 'alpha')); ?>"></td>
		</tr>
		<tr>
			<td><strong><?php echo $langs->trans('BarcodeValue'); ?>:</strong></td>
			<td><input type="text" id="barcode" name="barcode" class="takepospay" style="width:200px;" placeholder="<?php echo dol_escape_htmltag($langs->trans('BarcodeValue')); ?>" value="<?php echo dol_escape_htmltag(GETPOST('barcode', 'alpha')); ?>"></td>
		</tr>
		<tr>
			<td><strong><?php echo $langs->trans('Type'); ?>:</strong></td>
			<td>
				<select name="type" class="takepospay">
					<option value="0" <?php echo (GETPOSTINT('type') == 0 ? 'selected' : ''); ?>><?php echo $langs->trans('Product'); ?></option>
					<option value="1" <?php echo (GETPOSTINT('type') == 1 ? 'selected' : ''); ?>><?php echo $langs->trans('Service'); ?></option>
				</select>
			</td>
		</tr>
		<tr>
			<td><strong><?php echo $langs->trans('Price'); ?> (<?php echo $langs->trans('HT'); ?>):</strong></td>
			<td><input type="number" id="price" name="price" class="takepospay" style="width:150px;" step="0.01" placeholder="0.00" value="<?php echo GETPOSTFLOAT('price'); ?>"></td>
		</tr>
		<?php if (!empty($allcategories)) { ?>
		<tr>
			<td><strong><?php echo $langs->trans('Category'); ?>:</strong></td>
			<td>
				<select name="category" class="takepospay">
					<option value=""><?php echo $langs->trans('None'); ?></option>
					<?php
					foreach ($allcategories as $cat) {
						$selected = (GETPOSTINT('category') == $cat['id']) ? 'selected' : '';
						$indent = str_repeat('&nbsp;&nbsp;', ($cat['level'] - 1));
						echo '<option value="'.$cat['id'].'" '.$selected.'>'.$indent.dol_escape_htmltag($cat['label']).'</option>';
					}
					?>
				</select>
			</td>
		</tr>
		<?php } ?>
		<tr>
			<td colspan="2" style="text-align: center; padding-top: 20px;">
				<input type="submit" class="button takepospay" value="<?php echo dol_escape_htmltag($langs->trans('Create')); ?>" onclick="return Save();">
				<input type="button" class="button takepospay" value="<?php echo dol_escape_htmltag($langs->trans('Cancel')); ?>" onclick="parent.$.colorbox.close();">
			</td>
		</tr>
	</table>
</form>

</center>

</body>
</html>